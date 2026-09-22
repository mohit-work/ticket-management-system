import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from .contracts import CASES_CONTRACT, EMPLOYEES_CONTRACT, POLICIES_CONTRACT
from .quality import profile, validate
from .sources import ingest_sources
from .transform import (
    build_curated,
    standardize_cases,
    standardize_employees,
    standardize_policies,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PipelineConfig:
    input_dir: Path
    output_dir: Path
    api_url: str | None = None
    database_url: str | None = None
    incremental: bool = False


@dataclass
class PipelineResult:
    batch_id: str
    curated_rows: int
    rejected_rows: int
    reconciliation_passed: bool
    manifest_path: Path


def _write(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def _load_processed_case_ids(output_dir: Path) -> set[int]:
    state_path = output_dir / "state" / "processed_cases.csv"

    if not state_path.exists():
        return set()

    state = pd.read_csv(state_path)

    if "case_id" not in state.columns:
        return set()

    return set(pd.to_numeric(state["case_id"], errors="coerce").dropna().astype(int))


def _save_processed_case_ids(
    output_dir: Path,
    case_ids: pd.Series,
) -> None:
    state_path = output_dir / "state" / "processed_cases.csv"
    state_path.parent.mkdir(parents=True, exist_ok=True)

    new_ids = pd.to_numeric(case_ids, errors="coerce").dropna().astype(int)

    if state_path.exists():
        existing = pd.read_csv(state_path)
        existing_ids = (
            pd.to_numeric(existing["case_id"], errors="coerce")
            .dropna()
            .astype(int)
        )
        all_ids = pd.concat(
            [existing_ids, new_ids],
            ignore_index=True,
        ).drop_duplicates()
    else:
        all_ids = new_ids.drop_duplicates()

    pd.DataFrame({"case_id": sorted(all_ids.tolist())}).to_csv(
        state_path,
        index=False,
    )


def run_pipeline(config: PipelineConfig) -> PipelineResult:
    started_at = datetime.now(UTC)

    sources = ingest_sources(
        config.input_dir,
        config.api_url,
        config.database_url,
    )

    batch_id = hashlib.sha256(
        json.dumps(
            {name: source.to_json() for name, source in sources.items()},
            sort_keys=True,
        ).encode()
    ).hexdigest()[:16]

    batch_dir = config.output_dir / batch_id
    (batch_dir / "raw").mkdir(parents=True, exist_ok=True)

    for name, frame in sources.items():
        _write(frame, batch_dir / "raw" / f"{name}.csv")

    standardized = {
        "cases": standardize_cases(sources["cases"]),
        "employees": standardize_employees(sources["employees"]),
        "policies": standardize_policies(sources["policies"]),
    }

    contracts = {
        "cases": CASES_CONTRACT,
        "employees": EMPLOYEES_CONTRACT,
        "policies": POLICIES_CONTRACT,
    }

    accepted: dict[str, pd.DataFrame] = {}
    rejected_frames: list[pd.DataFrame] = []
    quality_report: dict[str, object] = {}

    for name, frame in standardized.items():
        _write(
            frame,
            batch_dir / "standardized" / f"{name}.csv",
        )

        result = validate(frame, contracts[name])
        accepted[name] = result.accepted

        if not result.rejected.empty:
            result.rejected.insert(0, "source_name", name)
            rejected_frames.append(result.rejected)

        quality_report[name] = {
            "profile": profile(frame, contracts[name]),
            **result.metrics,
        }

    cases_before_incremental = len(accepted["cases"])
    skipped_rows = 0

    if config.incremental:
        processed_case_ids = _load_processed_case_ids(config.output_dir)

        new_cases = accepted["cases"][
            ~accepted["cases"]["case_id"].isin(processed_case_ids)
        ].copy()

        skipped_rows = cases_before_incremental - len(new_cases)
        accepted["cases"] = new_cases

    curated = build_curated(
        accepted["cases"],
        accepted["employees"],
        accepted["policies"],
    )

    referential_rejects = curated.loc[
        ~curated["referential_integrity_valid"]
    ].copy()

    if not referential_rejects.empty:
        referential_rejects.insert(0, "source_name", "cases")
        referential_rejects["rejection_reason"] = (
            "referential integrity failure"
        )
        rejected_frames.append(referential_rejects)

    curated = curated.loc[
        curated["referential_integrity_valid"]
    ].drop(columns="referential_integrity_valid")

    rejected = (
        pd.concat(rejected_frames, ignore_index=True)
        if rejected_frames
        else pd.DataFrame()
    )

    _write(
        curated,
        batch_dir / "curated" / "cases.csv",
    )

    _write(
        rejected,
        batch_dir / "rejected" / "records.csv",
    )

    if config.incremental and not curated.empty:
        _save_processed_case_ids(
            config.output_dir,
            curated["case_id"],
        )

    source_rows = sum(
        len(frame)
        for frame in sources.values()
    )

    accounted_rows = (
        len(curated)
        + len(rejected)
        + skipped_rows
        + len(accepted["employees"])
        + len(accepted["policies"])
    )

    reconciliation_passed = (
        source_rows == accounted_rows
    )

    finished_at = datetime.now(UTC)

    manifest = {
        "batch_id": batch_id,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "incremental": config.incremental,
        "source_rows": source_rows,
        "standardized_rows": sum(
            len(frame)
            for frame in standardized.values()
        ),
        "curated_rows": len(curated),
        "rejected_rows": len(rejected),
        "skipped_rows": skipped_rows,
        "reconciliation": {
            "accounted_rows": accounted_rows,
            "passed": reconciliation_passed,
        },
        "contracts": {
            name: {
                "name": contract.name,
                "version": contract.version,
            }
            for name, contract in contracts.items()
        },
        "quality": quality_report,
    }

    manifest_path = batch_dir / "manifest.json"

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    logger.info(
        "pipeline batch=%s curated_rows=%s rejected_rows=%s skipped_rows=%s",
        batch_id,
        len(curated),
        len(rejected),
        skipped_rows,
    )

    return PipelineResult(
        batch_id,
        len(curated),
        len(rejected),
        reconciliation_passed,
        manifest_path,
    )