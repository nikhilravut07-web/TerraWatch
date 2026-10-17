from pydantic import BaseModel, Field
from typing import Literal, Any

Priority = Literal['critical-review','high-review','watch','routine','insufficient-evidence']
class Asset(BaseModel):
    id: str
    name: str
    category: str
    latitude: float
    longitude: float
    district: str
    buffer_m: int = 100
    review_status: str = 'Needs review'
    demo: bool = True
    description: str = ''
class Observation(BaseModel):
    id: str
    asset_id: str
    date: str
    source: str
    ndwi: float | None = None
    ndvi: float | None = None
    water_change_pct: float | None = None
    vegetation_change_pct: float | None = None
    quality: str
    quality_notes: list[str] = []
    demo: bool = True
class InvestigationRequest(BaseModel):
    mode: Literal['deterministic','llm'] = 'deterministic'
    question: str = Field(default='Assess environmental change and recommend a field check.', max_length=500)
class ToolExecution(BaseModel):
    tool: str
    status: str
    summary: str
    result: dict[str, Any] = {}
class Investigation(BaseModel):
    id: str
    asset_id: str
    mode: str
    status: str
    priority: Priority
    score: int | None
    rationale: list[str]
    uncertainty: list[str]
    recommended_action: str
    observations: list[dict[str, Any]]
    tool_trace: list[ToolExecution]
    created_at: str
    demo: bool = True
