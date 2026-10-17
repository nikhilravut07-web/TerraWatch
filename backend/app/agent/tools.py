from app import storage
from app.pipeline.indices import percent_change

def get_asset_details(asset_id):
    a=storage.get_asset(asset_id)
    return {'asset':a} if a else {'error':'asset_not_found'}
def search_satellite_observations(asset_id):
    return {'observations':storage.observations(asset_id),'source_mode':'stored_records_only'}
def check_observation_quality(observations):
    good=[o for o in observations if o.get('quality')=='good']
    warnings=[{'date':o.get('date'),'notes':o.get('quality_notes',[])} for o in observations if o.get('quality')!='good']
    return {'usable_count':len(good),'total_count':len(observations),'warnings':warnings,'sufficient':len(good)>=2}
def calculate_change_indicators(observations):
    usable=[o for o in observations if o.get('quality')=='good']
    if len(usable)<2: return {'available':False,'reason':'Fewer than two good-quality observations.'}
    first,last=usable[0],usable[-1]
    return {'available':True,'from_date':first['date'],'to_date':last['date'],'water_change_pct':last.get('water_change_pct'),'vegetation_change_pct':last.get('vegetation_change_pct'),'ndwi_delta':round(last['ndwi']-first['ndwi'],3) if last.get('ndwi') is not None and first.get('ndwi') is not None else None,'ndvi_delta':round(last['ndvi']-first['ndvi'],3) if last.get('ndvi') is not None and first.get('ndvi') is not None else None}
def get_rainfall_context(asset_id): return {'available':False,'value_mm':None,'reason':'No verified rainfall feed configured; rainfall is not inferred.'}
def get_terrain_context(asset_id): return {'available':False,'slope_degrees':None,'reason':'No elevation raster/context provider configured.'}
def calculate_priority_score(change,quality,rain,terrain):
    if not quality['sufficient'] or not change.get('available'):
        return {'score':None,'priority':'insufficient-evidence','factors':[],'reason':'Insufficient good-quality temporal evidence.'}
    factors=[]; score=20
    wc=change.get('water_change_pct')
    if wc is not None:
        impact=min(abs(wc),60)/60*40; score+=impact; factors.append({'factor':'absolute water indicator change','value_pct':wc,'points':round(impact,1)})
    vc=change.get('vegetation_change_pct')
    if vc is not None:
        impact=min(abs(vc),60)/60*20; score+=impact; factors.append({'factor':'absolute vegetation indicator change','value_pct':vc,'points':round(impact,1)})
    factors.append({'factor':'baseline evidence','points':10})
    score=min(100,round(score))
    priority='high-review' if score>=55 else 'watch' if score>=35 else 'routine'
    return {'score':score,'priority':priority,'factors':factors,'reason':'Transparent heuristic for triaging field checks; not a failure probability.'}
TOOLS={'get_asset_details':get_asset_details,'search_satellite_observations':search_satellite_observations,'check_observation_quality':check_observation_quality,'calculate_change_indicators':calculate_change_indicators,'get_rainfall_context':get_rainfall_context,'get_terrain_context':get_terrain_context,'calculate_priority_score':calculate_priority_score}
