import sys
import joblib
import os
import mlflow
import mlflow.sklearn

from sklearn.model_selection import (
    train_test_split
)

from sklearn.linear_model import (
    LinearRegression
)

from sklearn.ensemble import (
    RandomForestRegressor
)

from src.utils.logger import logger
from src.utils.exception import CustomException
from src.utils.mlflow_config import configure_mlflow

from src.models.regression.evaluate import (
    RegressionEvaluator
)

class FlightPriceTrainer:
    def train_models(
        self,
        X,
        y,
        preprocessor
    ):

        try:
            logger.info(
                "Starting train-test split"
            )

            X_train, X_test, y_train, y_test = (
                train_test_split(
                    X,
                    y,
                    test_size=0.2,
                    random_state=42
                )
            )

            logger.info(
                "Train-test split completed"
            )

            models = {
                "LinearRegression":
                    LinearRegression(),

                "RandomForest":
                    RandomForestRegressor(
                        n_estimators=100,
                        random_state=42
                    )
            }

            evaluator = RegressionEvaluator()

            model_report = {}

            best_model = None
            best_r2 = -1

            # Set tracking URI and experiment
            if mlflow.active_run():
                mlflow.end_run()

            configure_mlflow()
            mlflow.set_experiment(
                "Flight_Price_Prediction"
            )

            for model_name, model in models.items():
                with mlflow.start_run(
                    run_name = model_name
                ):

                    logger.info(
                        f"Training {model_name}"
                    )

                    model.fit(
                        X_train,
                        y_train
                    )

                    predictions = model.predict(
                        X_test
                    )

                    metrics = evaluator.evaluate_model(
                        y_test,
                        predictions
                    )

                    # Log params
                    mlflow.log_param("model_name", model_name)

                    if model_name == "RandomForest":
                        mlflow.log_param(
                            "n_estimators", 100
                        )

                    mlflow.log_param(
                        "random_state", 42
                    )
                
                    mlflow.log_param(
                        "dataset_version",
                        "v1.0.0"
                    )

                    # Log metrics
                    mlflow.log_metric("MAE", metrics["MAE"])    
                    mlflow.log_metric("RMSE", metrics["RMSE"])
                    mlflow.log_metric("R2_SCORE", metrics["R2_SCORE"])

                    # Log model
                    mlflow.sklearn.log_model(
                        model,
                        name=model_name
                    )

                    model_report[model_name] = metrics

                    logger.info(
                        f"{model_name} metrics: "
                        f"{metrics}"
                    )

                    if metrics["R2_SCORE"] > best_r2:

                        best_r2 = metrics["R2_SCORE"]

                        best_model = model

            logger.info(
                "Saving best regression model"
            )

            os.makedirs(
                "artifacts/models",
                exist_ok=True
            )

            joblib.dump(
                best_model,
                "artifacts/models/best_flight_price_model.pkl"
            )

            joblib.dump(
                X_train,
                "artifacts/models/training_features.pkl"
            )

            joblib.dump(
                preprocessor,
                "artifacts/models/preprocessor.pkl"
            )

            logger.info(
                "Model training completed"
            )

            return model_report

        except Exception as e:
            raise CustomException(e, sys)