import logging
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from app.config import settings
from app.database import engine
from app.models import Base, TnvedCode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

COLUMN_MAP = {
    0: "code",
    1: "name",
    2: "tariff",
    3: "details",
    4: "unit",
    5: "notes",
}


def import_excel(file_path: str) -> None:
    path = Path(file_path)
    if not path.exists():
        logger.error("Файл не найден: %s", path)
        sys.exit(1)

    logger.info("Чтение файла: %s", path)
    df = pd.read_excel(path, dtype=str)
    df = df.fillna("")

    rename = {}
    for i, col in enumerate(df.columns):
        if i in COLUMN_MAP:
            rename[col] = COLUMN_MAP[i]
    df = df.rename(columns=rename)

    for col in COLUMN_MAP.values():
        if col not in df.columns:
            df[col] = ""

    df = df[list(COLUMN_MAP.values())]
    df["code"] = df["code"].str.strip()
    df = df[df["code"] != ""]
    df = df.drop_duplicates(subset=["code"], keep="last")

    logger.info("Найдено строк: %d", len(df))

    data_dir = Path(settings.database_url.replace("sqlite:///", "")).parent
    data_dir.mkdir(parents=True, exist_ok=True)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        records = df.to_dict(orient="records")
        if records:
            conn.execute(TnvedCode.__table__.insert(), records)

    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM tnved_codes")).scalar()
        logger.info("Импортировано записей: %d", count)

    logger.info("Импорт завершён успешно")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python import_excel.py <путь_к_файлу.xlsx>")
        sys.exit(1)
    import_excel(sys.argv[1])
