from uuid import uuid4
from datetime import datetime, timezone
from app.agent.tools import TOOLS
from app import storage

MAX_TOOL_CALLS=7

def investigate(asset_id: str, mode: str='deterministic', question: str=''):
    if mode=='llm':
        raise ValueError('LLM mode is unavailable: no provider integration/credentials configured. Choose deterministic mode.')
    trace=[]; calls=0
    def run(name,*args):
        nonlocal calls
        if calls>=MAX_TOOL_CALLS: raise RuntimeError('Tool-call budget exceeded')
        calls+=1
        try:
            result=TOOLS[name](*args); trace.append({'tool':name,'status':'ok','summary':_summary(name,result),'result':result}); return result
        except Exception as e:
            trace.append({'tool':name,'status':'error','summary':str(e),'result':{}}); return {'error':str(e)}
    ares=run('get_asset_details',asset_id); asset=ares.get('asset')
    if not asset: return None
    obsres=run('search_satellite_observations',asset_id); obs=obsres.get('observations',[])
    quality=run('check_observation_quality',obs)
    change=run('calculate_change_indicators',obs)
    rain=run('get_rainfall_context',asset_id); terrain=run('get_terrain_context',asset_id)
    scoring=run('calculate_priority_score',change,quality,rain,terrain)
    uncertainties=[]
    if quality['warnings']: uncertainties.append('One or more observations have quality warnings; seasonal and atmospheric effects remain possible.')
    if not rain['available']: uncertainties.append(rain['reason'])
    if not terrain['available']: uncertainties.append(terrain['reason'])
    if not quality['sufficient']: uncertainties.append('Fewer than two good-quality observations; no confident change assessment is made.')
    if change.get('available') and change.get('water_change_pct') is not None: uncertainties.append('Water-indicator change can reflect seasonality, rainfall, turbidity, shadows or residual cloud—not necessarily infrastructure damage.')
    priority=scoring['priority']
    action=('Field engineer should inspect the asset and adjacent drainage/embankment, document visible erosion or blockage, and compare with local rainfall/maintenance records.' if priority in ('high-review','watch') else 'Review available evidence and obtain a fresh clear observation before deciding whether a field visit is warranted.' if priority=='insufficient-evidence' else 'Continue routine monitoring; no urgent field action is indicated by this limited environmental evidence.')
    report={'id':str(uuid4()),'asset_id':asset_id,'mode':'deterministic','status':'abstained' if priority=='insufficient-evidence' else 'completed','priority':priority,'score':scoring['score'],'rationale':[scoring['reason']]+[f"{f['factor']}: {f.get('value_pct',f.get('points'))}" for f in scoring.get('factors',[])],'uncertainty':uncertainties,'recommended_action':action,'observations':obs,'tool_trace':trace,'created_at':datetime.now(timezone.utc).isoformat(),'demo':all(o.get('demo',True) for o in obs),'context':{'rainfall':rain,'terrain':terrain,'change':change,'quality':quality,'scoring':scoring},'question':question}
    storage.save_investigation(report); return report

def _summary(name,r):
    if 'error' in r: return r['error']
    if name=='get_asset_details': return 'Loaded asset metadata.'
    if name=='search_satellite_observations': return f"Found {len(r.get('observations',[]))} stored observations."
    if name=='check_observation_quality': return f"{r.get('usable_count',0)} of {r.get('total_count',0)} observations pass quality checks."
    if name=='calculate_change_indicators': return 'Compared first and last usable observations.' if r.get('available') else r.get('reason','No change estimate.')
    if name in ('get_rainfall_context','get_terrain_context'): return r.get('reason','Context unavailable.')
    if name=='calculate_priority_score': return r.get('reason','Priority calculated.')
    return 'Tool completed.'
