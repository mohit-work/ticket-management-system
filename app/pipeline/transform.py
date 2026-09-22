import pandas as pd


def standardize_cases(cases: pd.DataFrame) -> pd.DataFrame:
    result = cases.copy()
    result.columns = [column.strip().lower() for column in result.columns]
    result["case_id"] = pd.to_numeric(result["case_id"], errors="coerce").astype("Int64")
    result["employee_id"] = pd.to_numeric(result["employee_id"], errors="coerce").astype("Int64")
    result["priority"] = result["priority"].astype("string").str.upper().str.strip()
    result["status"] = result["status"].astype("string").str.upper().str.strip()
    result["category"] = result["category"].astype("string").str.title().str.strip()
    result["created_at"] = pd.to_datetime(result["created_at"], errors="coerce", utc=True)
    return result


def standardize_employees(employees: pd.DataFrame) -> pd.DataFrame:
    result = employees.copy()
    result.columns = [column.strip().lower() for column in result.columns]
    result["employee_id"] = pd.to_numeric(result["employee_id"], errors="coerce").astype("Int64")
    result["employee_name"] = result["employee_name"].astype("string").str.strip()
    result["department"] = result["department"].astype("string").str.strip()
    return result


def standardize_policies(policies: pd.DataFrame) -> pd.DataFrame:
    result = policies.copy()
    result.columns = [column.strip().lower() for column in result.columns]
    result["priority"] = result["priority"].astype("string").str.upper().str.strip()
    result["sla_hours"] = pd.to_numeric(result["sla_hours"], errors="coerce")
    result["policy_version"] = result["policy_version"].astype("string").str.strip()
    return result


def filter_cases(cases: pd.DataFrame, status: str | None = None) -> pd.DataFrame:
    result = cases.copy()
    if status:
        result = result[result["status"].eq(status.upper())]
    return result


def aggregate_cases(cases: pd.DataFrame) -> pd.DataFrame:
    return (
        cases.groupby("priority", dropna=False)
        .agg(case_count=("case_id", "count"))
        .reset_index()
    )


def add_priority_rank(cases: pd.DataFrame) -> pd.DataFrame:
    result = cases.copy()
    priority_order = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
    result["priority_rank"] = result["priority"].map(priority_order)
    result["priority_rank"] = (
        result.groupby("employee_id")["priority_rank"]
        .rank(method="dense", ascending=True)
    )
    return result


def deduplicate_cases(cases: pd.DataFrame) -> pd.DataFrame:
    return cases.drop_duplicates(subset=["case_id"], keep="first").reset_index(drop=True)


def build_curated(
    cases: pd.DataFrame,
    employees: pd.DataFrame,
    policies: pd.DataFrame,
) -> pd.DataFrame:
    curated = cases.merge(
        employees,
        on="employee_id",
        how="left",
        validate="many_to_one",
    )
    curated = curated.merge(
        policies,
        on="priority",
        how="left",
        validate="many_to_one",
    )
    curated["referential_integrity_valid"] = (
        curated["employee_name"].notna() & curated["sla_hours"].notna()
    )
    curated["case_age_days"] = (
        (pd.Timestamp.now(tz="UTC") - curated["created_at"])
        .dt.total_seconds()
        .div(86400)
        .round(2)
    )
    return curated