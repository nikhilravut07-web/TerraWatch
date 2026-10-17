# TerraWatch

**Agentic environmental-change triage for rural infrastructure.** TerraWatch combines an asset inventory, time-indexed environmental indicators, evidence quality checks, a bounded tool-using investigation workflow, and a geospatial inspection-priority dashboard.

> **Safety and provenance:** TerraWatch is a human decision-support prototype. Sentinel-2 cannot confirm hairline cracks or hidden structural damage. Scores are heuristic triage scores, not validated probabilities of infrastructure failure. All bundled observations and asset locations are explicitly illustrative demo data, not verified incidents or actual satellite retrievals.

## Features

- React + TypeScript + Vite dashboard, Leaflet map, asset details, history charts, evidence quality labels, inspection queue, investigation trace and JSON report export.
- FastAPI + Pydantic API and persistent SQLite records.
- Bounded deterministic agent: asset lookup → observation retrieval → quality check → change indicators → rainfall context → terrain context → explainable score. Maximum seven tool calls; low-quality evidence triggers abstention.
- Tested NDWI / NDVI functions with invalid-pixel and alignment handling.
- Modular Earth Search STAC adapter at `GET /api/live/scenes`. This discovers Sentinel-2 L2A scenes from the public STAC endpoint; it does **not** download raster assets or calculate real-world indicators yet. The UI does not pretend it has done so.
- Live provider errors are returned explicitly; they are never silently replaced with demo results.

## Requirements

- Python 3.11+ (tested in this environment with Python 3.13)
- Node.js 20+ and npm
- Internet access is only needed to install npm packages, load OpenStreetMap tiles, or explicitly call the STAC discovery endpoint.

## Run locally

### Windows PowerShell

```powershell
cd terrawatch
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
$env:PYTHONPATH = "$PWD\backend"
uvicorn app.main:app --app-dir backend --reload --port 8000
```

In a second terminal:

```powershell
cd terrawatch\frontend
npm install
npm run dev
```

Open `http://localhost:5173`. API docs are at `http://127.0.0.1:8000/docs`.

### macOS / Linux

```bash
cd terrawatch
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
cd terrawatch/frontend
npm install
npm run dev
```

## API

- `GET /api/health`
- `GET /api/assets`
- `GET /api/assets/{asset_id}`
- `GET /api/assets/{asset_id}/observations`
- `POST /api/assets/{asset_id}/investigate` — JSON body: `{"mode":"deterministic","question":"Review the available evidence"}`
- `GET /api/investigations/{investigation_id}`
- `GET /api/inspection-queue`
- `GET /api/reports/{report_id}`
- `GET /api/live/scenes?bbox=73.7,18.4,74.0,18.7&start_date=2026-06-01&end_date=2026-09-30&limit=10`

The live scene endpoint uses Earth Search STAC and returns scene metadata only. Dates and bounding boxes must be supplied for the intended study area. It may fail when the provider is unavailable.

## Agent modes

The deterministic mode is a genuine bounded tool workflow but **is not an LLM agent**. No LLM credentials are assumed. Requests for `mode: "llm"` return an explicit unavailable error rather than pretending an LLM was used. A provider can be added behind the existing tool interface using environment-managed credentials, fixed tool schemas, call budgets and timeouts.

## Data sources and current implementation boundaries

- Demo assets and observation records: `data/demo/demo_data.json` (illustrative only).
- Live scene discovery: Earth Search STAC API (`https://earth-search.aws.element84.com/v1/search`), collection `sentinel-2-l2a`.
- Basemap: OpenStreetMap tile service in Leaflet.
- NDWI / NDVI: tested array-level calculation helpers; no real scene raster download, cloud-mask extraction or spatial alignment pipeline is wired into the UI yet.
- Rainfall and terrain: provider interfaces return an explicit unavailable status; no verified feeds are configured.

## Tests

From the repository root:

```bash
PYTHONPATH=backend pytest backend/tests -q
```

Frontend production build:

```bash
cd frontend
npm install
npm run build
```

## Limitations and responsible use

- Sample data is illustrative and cannot be used to make real infrastructure safety decisions.
- The score is a configurable heuristic, not a calibrated risk probability or validated engineering model.
- NDWI / NDVI can be affected by seasonality, shadows, turbidity, clouds, mixed pixels and other environmental effects.
- Sentinel-2 pixel resolution is not suitable for identifying hairline cracks or diagnosing hidden structural damage.
- No autonomous emergency dispatch, closure, or declaration that an asset is unsafe is implemented.
- Before any field deployment, validate coordinates, data licensing, observation processing, quality thresholds, score calibration and recommendations with qualified engineers and local authorities.

## GitHub publishing

This local prototype is prepared for review only. Do not publish until the tests/build and secret scan are reviewed, then confirm repository name, visibility and push action explicitly.

## Validation status for this packaged snapshot

- Backend tests: **11 passed** (`PYTHONPATH=backend pytest backend/tests -q`).
- Python syntax compilation: passed (`python -m compileall -q backend/app backend/tests`).
- Basic secret-pattern scan: no matches found.
- Frontend production build: **not verified in the build environment**. npm dependency installation timed out before packages were installed, so `npm run build` could not run successfully here. Run `npm install` and `npm run build` on a machine with npm registry access before treating the prototype as fully validated.
- Git: no repository was present initially. A local repository/commit has intentionally not been created because the frontend production build remains unverified. No remote repository was created and nothing was pushed.
