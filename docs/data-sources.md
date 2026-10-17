# Data sources and provenance

- **Bundled demo records:** `data/demo/demo_data.json`; all records are illustrative and explicitly marked `demo: true`.
- **Sentinel-2 discovery:** Earth Search STAC API, `sentinel-2-l2a`. The current adapter requests scene metadata only; it does not download imagery or compute live NDWI/NDVI.
- **Map tiles:** OpenStreetMap tile layer via Leaflet. Network availability and provider terms apply.
- **Rainfall and terrain:** not configured. API tool results explicitly mark these data as unavailable rather than fabricating values.

Keep data-provider boundaries explicit. Do not mix demo records with live measurements without source labels and provenance fields.
