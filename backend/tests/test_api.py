from fastapi.testclient import TestClient
from app.main import app

def test_health_and_assets():
    with TestClient(app) as client:
        assert client.get('/api/health').status_code==200
        assert len(client.get('/api/assets').json())==5

def test_investigation_endpoint():
    with TestClient(app) as client:
        r=client.post('/api/assets/TW-001/investigate',json={'mode':'deterministic'})
        assert r.status_code==200 and len(r.json()['tool_trace'])==7

def test_missing_and_validation():
    with TestClient(app) as client:
        assert client.get('/api/assets/nope').status_code==404
        assert client.get('/api/live/scenes',params={'bbox':'1,2'}).status_code==422
