from pathlib import Path

import mlflow

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def configure_mlflow() -> None:
    """Use a project-local MLflow store with portable absolute paths."""
    tracking_dir = PROJECT_ROOT / "mlruns"
    tracking_dir.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(tracking_dir.as_uri())
