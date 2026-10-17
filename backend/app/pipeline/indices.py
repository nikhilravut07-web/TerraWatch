import numpy as np

def _index(a,b):
    a=np.asarray(a,dtype=float); b=np.asarray(b,dtype=float)
    if a.shape != b.shape: raise ValueError('Band arrays must be aligned and have identical shapes')
    den=a+b
    out=np.full(a.shape,np.nan,dtype=float)
    valid=np.isfinite(a)&np.isfinite(b)&(np.abs(den)>1e-9)
    out[valid]=(a[valid]-b[valid])/den[valid]
    return out

def ndwi(green,nir): return _index(green,nir)
def ndvi(nir,red): return _index(nir,red)
def mean_valid(a):
    a=np.asarray(a,dtype=float); valid=a[np.isfinite(a)]
    return None if not valid.size else float(np.mean(valid))
def percent_change(before,after):
    if before is None or after is None: return None
    if abs(before)<1e-9: return None
    return round((after-before)/abs(before)*100,2)
