import json
import os

from src.data.bootstrap import ensure_users_csv
from src.data.ingestion import DataIngestion
from src.models.classification.preprocess import UserPreprocessor
from src.models.classification.train import GenderClassificationTrainer

ensure_users_csv()

users_df = DataIngestion().load_users_data()

preprocessor = UserPreprocessor()
X, y, fitted_preprocessor = preprocessor.preprocess_users_data(users_df)

trainer = GenderClassificationTrainer()
report = trainer.train_models(X, y, fitted_preprocessor)

os.makedirs("artifacts/metrics", exist_ok=True)

with open("artifacts/metrics/gender_classification_metrics.json", "w") as file:
    json.dump(report, file, indent=4)

print("Gender classification training complete")
print(json.dumps(report, indent=2))
