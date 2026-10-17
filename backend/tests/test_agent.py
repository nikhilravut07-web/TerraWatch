from app.agent.runner import investigate
from app import storage

def test_agent_traces_tools_and_persists():
    storage.init_db(); r=investigate('TW-001')
    assert r and r['mode']=='deterministic' and len(r['tool_trace'])==7
    assert r['id'] and storage.get_investigation(r['id'])['asset_id']=='TW-001'
def test_low_quality_abstains():
    storage.init_db(); r=investigate('TW-004')
    assert r['priority']=='insufficient-evidence' and r['score'] is None and r['status']=='abstained'
def test_llm_not_misrepresented():
    import pytest
    with pytest.raises(ValueError,match='no provider integration'): investigate('TW-001','llm')
def test_missing_asset(): assert investigate('missing') is None
