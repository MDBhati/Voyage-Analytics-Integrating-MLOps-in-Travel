import sys

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from src.utils.logger import logger
from src.utils.exception import CustomException

class RegressionEvaluator:
    def evaluate_model(
        self,
        y_true,
        y_pred
    ):

        try:
            logger.info(
                "Evaluating regression model"
            )

            mae = mean_absolute_error(
                y_true,
                y_pred
            )

            rmse = (
                mean_squared_error(
                    y_true,
                    y_pred
                ) ** 0.5
            )

            r2 = r2_score(
                y_true,
                y_pred
            )

            metrics = {
                "MAE": mae,
                "RMSE": rmse,
                "R2_SCORE": r2
            }

            logger.info(
                f"Evaluation metrics: {metrics}"
            )

            return metrics

        except Exception as e:
            raise CustomException(e, sys)