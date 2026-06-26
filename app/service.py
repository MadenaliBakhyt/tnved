from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import TnvedCode


def get_by_code(db: Session, code: str) -> TnvedCode | None:
    stmt = select(TnvedCode).where(TnvedCode.code == code)
    return db.execute(stmt).scalar_one_or_none()


def search_by_name(db: Session, query: str, limit: int | None = None) -> list[TnvedCode]:
    if limit is None:
        limit = settings.search_limit
    stmt = (
        select(TnvedCode)
        .where(func.LOWER_UTF8(TnvedCode.name).contains(query.lower()))
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())
