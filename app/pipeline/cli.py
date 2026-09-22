import argparse
import logging
from pathlib import Path

from .runner import PipelineConfig, run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the case-management data pipeline"
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/input"),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/output"),
    )

    parser.add_argument("--api-url")
    parser.add_argument("--database-url")
    parser.add_argument(
        "--incremental",
        action="store_true",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    result = run_pipeline(
        PipelineConfig(
            args.input_dir,
            args.output_dir,
            args.api_url,
            args.database_url,
            args.incremental,
        )
    )

    print(
        f"batch_id={result.batch_id} "
        f"curated_rows={result.curated_rows} "
        f"rejected_rows={result.rejected_rows} "
        f"reconciliation_passed={result.reconciliation_passed}"
    )


if __name__ == "__main__":
    main()