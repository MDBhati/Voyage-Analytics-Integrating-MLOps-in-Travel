import sys

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
)

from src.utils.logger import logger
from src.utils.exception import CustomException


class ClassificationEvaluator:

    def evaluate_model(self, y_true, y_pred):
        try:
            logger.info("Evaluating classification model")

            accuracy = accuracy_score(y_true, y_pred)
            f1 = f1_score(y_true, y_pred, average="weighted")

            metrics = {
                "accuracy": round(float(accuracy), 4),
                "f1_weighted": round(float(f1), 4),
            }

            logger.info(f"Evaluation metrics: {metrics}")
            logger.info(
                f"Classification report:\n"
                f"{classification_report(y_true, y_pred)}"
            )

            return metrics

        except Exception as e:
            raise CustomException(e, sys)
