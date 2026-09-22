from dataclasses import dataclass

import pandas as pd

from .contracts import DataContract


@dataclass
class QualityResult:
    accepted: pd.DataFrame
    rejected: pd.DataFrame
    metrics: dict[str, int | float]


def profile(frame: pd.DataFrame, contract: DataContract) -> dict[str, object]:
    completeness = frame.notna().mean().round(4).to_dict()
    uniqueness = {
        column: int(frame[column].nunique(dropna=False))
        for column in contract.unique_columns
        if column in frame
    }

    validity = {}
    if "priority" in frame:
        valid_priorities = {"HIGH", "MEDIUM", "LOW"}
        validity["priority"] = round(
            frame["priority"].isin(valid_priorities).mean(),
            4,
        )

    if "status" in frame:
        valid_statuses = {
            "OPEN",
            "ASSIGNED",
            "IN_PROGRESS",
            "RESOLVED",
            "CLOSED",
        }
        validity["status"] = round(
            frame["status"].isin(valid_statuses).mean(),
            4,
        )

    distribution = {}
    for column in ("priority", "status", "category", "department"):
        if column in frame:
            distribution[column] = frame[column].value_counts(
                dropna=False
            ).to_dict()

    return {
        "rows": int(len(frame)),
        "columns": list(frame.columns),
        "completeness": completeness,
        "unique_values": uniqueness,
        "validity": validity,
        "distribution": distribution,
    }


def validate(frame: pd.DataFrame, contract: DataContract) -> QualityResult:
    errors = pd.Series("", index=frame.index, dtype="object")

    for message in contract.validate_columns(frame):
        errors.loc[:] = errors + ("; " if errors.any() else "") + message

    if not frame.empty:
        for column in contract.required_columns:
            if column in frame:
                missing = (
                    frame[column].isna()
                    | frame[column].astype(str).str.strip().eq("")
                )
                errors.loc[missing] = (
                    errors.loc[missing]
                    + ("; " if errors.loc[missing].ne("").any() else "")
                    + f"missing value: {column}"
                )

        for column in contract.unique_columns:
            if column in frame:
                duplicate = frame[column].duplicated(keep=False)
                errors.loc[duplicate] = (
                    errors.loc[duplicate]
                    + ("; " if errors.loc[duplicate].ne("").any() else "")
                    + f"duplicate value: {column}"
                )

    rejected = frame.loc[errors.ne("")].copy()
    rejected["rejection_reason"] = errors.loc[errors.ne("")]
    accepted = frame.loc[errors.eq("")].copy()

    return QualityResult(
        accepted=accepted,
        rejected=rejected,
        metrics={
            "input_rows": len(frame),
            "accepted_rows": len(accepted),
            "rejected_rows": len(rejected),
        },
    )