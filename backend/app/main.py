from contextlib import asynccontextmanager
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app import storage
from app.models import InvestigationRequest
from app.agent.runner import investigate
from app.services.stac import search_scenes

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.init_db(); yield
app=FastAPI(title='TerraWatch API',version='0.1.0',description='Evidence-linked environmental change triage; not structural diagnosis.',lifespan=lifespan)
_default_origins = 'http://localhost:5173,http://127.0.0.1:5173'
_allowed_origins = [origin.strip().rstrip('/') for origin in os.getenv('TERRAWATCH_CORS_ORIGINS', _default_origins).split(',') if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=_allowed_origins, allow_credentials=False, allow_methods=['GET','POST','OPTIONS'], allow_headers=['*'])
@app.get('/api/health')
def health(): return {'status':'ok','mode':'demo-capable','database':'sqlite','llm_configured':False}
@app.get('/api/assets')
def list_assets(): return storage.assets()
@app.get('/api/assets/{asset_id}')
def get_asset(asset_id):
    a=storage.get_asset(asset_id)
    if not a: raise HTTPException(404,'Asset not found')
    return a
@app.get('/api/assets/{asset_id}/observations')
def get_observations(asset_id):
    if not storage.get_asset(asset_id): raise HTTPException(404,'Asset not found')
    return storage.observations(asset_id)
@app.post('/api/assets/{asset_id}/investigate')
def run_investigation(asset_id,req: InvestigationRequest):
    try: report=investigate(asset_id,req.mode,req.question)
    except ValueError as e: raise HTTPException(400,str(e))
    if not report: raise HTTPException(404,'Asset not found')
    return report
@app.get('/api/investigations/{investigation_id}')
def investigation_detail(investigation_id):
    r=storage.get_investigation(investigation_id)
    if not r: raise HTTPException(404,'Investigation not found')
    return r
@app.get('/api/inspection-queue')
def inspection_queue():
    reports=storage.all_investigations(); latest={}
    for r in reports: latest.setdefault(r['asset_id'],r)
    order={'high-review':0,'watch':1,'insufficient-evidence':2,'routine':3,'critical-review':0}
    return sorted(latest.values(),key=lambda r:(order.get(r['priority'],9),-(r['score'] or 0)))
@app.get('/api/reports/{report_id}')
def report_detail(report_id): return investigation_detail(report_id)
@app.get('/api/live/scenes')
async def live_scenes(bbox: str=Query(...,description='west,south,east,north'),start_date: str='2024-01-01',end_date: str='2024-12-31',limit: int=10):
    try:
        coords=[float(x.strip()) for x in bbox.split(',')]
        if len(coords)!=4 or coords[0]>=coords[2] or coords[1]>=coords[3]: raise ValueError()
        return {'mode':'live-stac','scenes':await search_scenes(coords,start_date,end_date,limit)}
    except ValueError: raise HTTPException(422,'bbox must be west,south,east,north and have increasing bounds')
    except Exception as e: raise HTTPException(502,f'STAC provider unavailable: {type(e).__name__}; no demo substitution was made')
