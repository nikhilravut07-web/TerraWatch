# Limitations and safety

1. This is a hackathon prototype for inspection prioritisation, not structural diagnosis.
2. Satellite indicators cannot identify hairline cracks or confirm hidden damage.
3. Bundled coordinates, assets and observation measurements are illustrative, not verified incidents or downloaded satellite data.
4. NDWI/NDVI functions operate on arrays; actual satellite raster retrieval, cloud masking and aligned multi-date processing are not yet integrated.
5. The priority score is heuristic and is not a validated probability of failure.
6. Rainfall and terrain context providers are unavailable; missing information remains missing.
7. Deterministic tool orchestration is not represented as an LLM agent. LLM mode is explicitly unavailable until a provider is integrated.
8. The system cannot declare an asset unsafe, close a road or dispatch emergency services.
9. Any operational use requires qualified engineering review, verified asset coordinates, validated imagery and quality controls, and locally calibrated scoring.
