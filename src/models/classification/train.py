import os
import sys
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from src.utils.logger import logger
from src.utils.exception import CustomException
from src.utils.mlflow_config import configure_mlflow
from src.models.classification.evaluate import ClassificationEvaluator


class GenderClassificationTrainer:

    def train_models(self, X, y, preprocessor):
        try:
            logger.info("Starting gender classification train-test split")

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42,
                stratify=y,
            )

            models = {
                "LogisticRegression": LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
                "RandomForest": RandomForestClassifier(
                    n_estimators=100,
                    random_state=42,
                ),
            }

            evaluator = ClassificationEvaluator()
            model_report = {}
            best_model = None
            best_f1 = -1.0

            if mlflow.active_run():
                mlflow.end_run()

            configure_mlflow()
            mlflow.set_experiment("Gender_Classification")

            for model_name, model in models.items():
                with mlflow.start_run(run_name=model_name):
                    logger.info(f"Training {model_name}")

                    model.fit(X_train, y_train)
                    predictions = model.predict(X_test)
                    metrics = evaluator.evaluate_model(y_test, predictions)

                    mlflow.log_param("model_name", model_name)
                    mlflow.log_metric("accuracy", metrics["accuracy"])
                    mlflow.log_metric("f1_weighted", metrics["f1_weighted"])
                    mlflow.sklearn.log_model(model, name=model_name)

                    model_report[model_name] = metrics

                    if metrics["f1_weighted"] > best_f1:
                        best_f1 = metrics["f1_weighted"]
                        best_model = model

            os.makedirs("artifacts/models", exist_ok=True)

            joblib.dump(
                best_model,
                "artifacts/models/gender_classifier.pkl",
            )
            joblib.dump(
                preprocessor,
                "artifacts/models/gender_classifier_preprocessor.pkl",
            )

            logger.info(
                f"Best gender classifier saved (f1_weighted={best_f1:.4f})"
            )

            return model_report

        except Exception as e:
            raise CustomException(e, sys)
