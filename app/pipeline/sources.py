import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen

import pandas as pd
from sqlalchemy import create_engine


def read_file(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix == ".json":
        payload: Any = json.loads(path.read_text(encoding="utf-8"))
        return pd.DataFrame(payload.get("data", payload) if isinstance(payload, dict) else payload)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported source format: {path.suffix}")


def read_rest_api(url: str, timeout: int = 30) -> pd.DataFrame:
    with urlopen(url, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    records = payload.get("data", payload) if isinstance(payload, dict) else payload
    return pd.DataFrame(records)


def read_sql_table(database_url: str, table_name: str) -> pd.DataFrame:
    engine = create_engine(database_url)
    result = pd.read_sql_table(table_name, engine)

    if table_name == "tickets":
        result = result.rename(columns={"id": "case_id"})

    return result


def ingest_sources(
    input_dir: Path,
    api_url: str | None = None,
    database_url: str | None = None,
) -> dict[str, pd.DataFrame]:
    sources = {
        "cases": read_file(input_dir / "cases.csv"),
        "employees": read_file(input_dir / "employees.json"),
        "policies": read_file(input_dir / "policies.csv"),
    }

    if api_url:
        sources["policies"] = read_rest_api(api_url)

    if database_url:
        sources["cases"] = read_sql_table(database_url, "tickets")

    return sources