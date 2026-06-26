from pydantic import BaseModel


class TnvedCodeResponse(BaseModel):
    code: str
    name: str | None = None
    tariff: str | None = None
    details: str | None = None
    unit: str | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}


class SearchResponse(BaseModel):
    total: int
    results: list[TnvedCodeResponse]
