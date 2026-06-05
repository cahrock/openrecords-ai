from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class ClassificationRequest(BaseModel):
    foia_request_id: UUID
    subject: str
    description: str
    records_requested: str


class ClassificationResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    foia_request_id: UUID
    suggested_category: str
    suggested_priority: str = Field(description="LOW, MEDIUM, or HIGH")
    confidence_score: float = Field(ge=0.0, le=1.0)
    model_id: str
    raw_response: str