"""Earth Search STAC adapter. Network calls are opt-in and never replaced by demo data silently."""
import httpx
STAC_URL='https://earth-search.aws.element84.com/v1/search'
async def search_scenes(bbox: list[float], start_date: str, end_date: str, limit: int=10):
    payload={'collections':['sentinel-2-l2a'],'bbox':bbox,'datetime':f'{start_date}T00:00:00Z/{end_date}T23:59:59Z','limit':min(max(limit,1),50)}
    async with httpx.AsyncClient(timeout=12) as client:
        response=await client.post(STAC_URL,json=payload); response.raise_for_status(); body=response.json()
    return [{'id':f['id'],'date':f.get('properties',{}).get('datetime'),'cloud_cover':f.get('properties',{}).get('eo:cloud_cover'),'collection':f.get('collection'),'assets':list(f.get('assets',{}).keys())} for f in body.get('features',[])]
