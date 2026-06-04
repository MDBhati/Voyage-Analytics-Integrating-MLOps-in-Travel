from src.pipelines.training_pipeline import (
    TrainingPipeline
)

import json
import os

pipeline = TrainingPipeline()

report = pipeline.run_pipeline()

os.makedirs(
    "artifacts/metrics",
    exist_ok=True
)

with open(
    "artifacts/metrics/model_metrics.json",
    "w"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )

print(report)