from dataclasses import dataclass
from typing import Any

import pandas as pd



@dataclass(frozen=True)
class DataContract:
    name: str
    version: str
    required_columns: tuple[str, ...]
    unique_columns: tuple[str, ...] = ()

    def validate_columns(self, frame: pd.DataFrame) -> list[str]:
        missing = [column for column in self.required_columns if column not in frame.columns]
        return [f"missing column: {column}" for column in missing]


CASES_CONTRACT = DataContract(
    name="cases",
    version="1.0",
    required_columns=(
        "case_id", "employee_id", "title", "category", "priority", "status",
        "created_at",
    ),
    unique_columns=("case_id",),
)

EMPLOYEES_CONTRACT = DataContract(
    name="employees",
    version="1.0",
    required_columns=("employee_id", "employee_name", "department"),
    unique_columns=("employee_id",),
)

POLICIES_CONTRACT = DataContract(
    name="policies",
    version="1.0",
    required_columns=("priority", "sla_hours", "policy_version"),
    unique_columns=("priority",),
)


def as_json_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return frame.where(frame.notna(), None).to_dict(orient="records")