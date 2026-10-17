# Architecture

```text
React + TypeScript + Vite
  ├─ Leaflet map and asset selection
  ├─ observation timeline and evidence panel
  ├─ investigation trace and report export
  └─ FastAPI JSON API
       ├─ Pydantic request validation
       ├─ SQLite storage
       ├─ deterministic bounded agent (max 7 calls)
       │    ├─ asset / observation tools
       │    ├─ quality gate and change comparison
       │    ├─ rainfall / terrain unavailable adapters
       │    └─ transparent priority heuristic + abstention
       └─ optional Earth Search STAC scene discovery
```

SQLite is initialised from `data/demo/demo_data.json` on first run. Investigation reports are persisted. Demo observations are never presented as live STAC-derived observations. The STAC adapter currently discovers metadata only; raster download, masking, spatial alignment and index computation over actual Sentinel-2 assets remain future implementation work.
