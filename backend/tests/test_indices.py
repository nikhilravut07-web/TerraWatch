import numpy as np, pytest
from app.pipeline.indices import ndwi, ndvi, percent_change

def test_ndwi_controlled():
    out=ndwi(np.array([3.,1.,np.nan]),np.array([1.,3.,2.]))
    assert out[0]==pytest.approx(.5); assert out[1]==pytest.approx(-.5); assert np.isnan(out[2])
def test_ndvi(): assert ndvi([.8,.2],[.2,.2]).tolist()==pytest.approx([.6/1,.0])
def test_alignment():
    with pytest.raises(ValueError): ndwi([1,2],[1])
def test_percent_change(): assert percent_change(10,15)==50; assert percent_change(0,2) is None
