import logging

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas import SearchResponse, TnvedCodeResponse
from app.service import get_by_code, search_by_name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)


@app.get("/code/{code}", response_model=TnvedCodeResponse)
def get_code(code: str, db: Session = Depends(get_db)):
    result = get_by_code(db, code)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Код {code} не найден")
    return result


@app.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1, description="Поисковый запрос по наименованию"),
    limit: int = Query(default=50, ge=1, le=200, description="Максимальное количество результатов"),
    db: Session = Depends(get_db),
):
    results = search_by_name(db, q, limit)
    return SearchResponse(total=len(results), results=results)


@app.get("/health")
def health():
    return {"status": "ok"}
