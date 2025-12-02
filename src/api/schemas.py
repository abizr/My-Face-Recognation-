from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class BaseSchema(BaseModel):
    model_config = ConfigDict(protected_namespaces=())


class PersonMeta(BaseSchema):
    name: str
    email: Optional[str] = None
    labels: Optional[Dict[str, Any]] = None


class EnrollResponse(BaseSchema):
    person_id: UUID
    sample_id: UUID
    embedding_dim: int
    model_version: str


class VerifyResponse(BaseSchema):
    match: bool
    score: float
    threshold: float
    model_version: str


class SearchResult(BaseSchema):
    person_id: UUID
    score: float
    image_uri: str


class SearchResponse(BaseSchema):
    results: List[SearchResult] = Field(default_factory=list)
    model_version: str


class HealthStatus(BaseSchema):
    status: str
    db: str
    storage: str
    model_version: str
