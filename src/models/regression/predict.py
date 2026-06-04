import sys
import joblib
import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException

class FlightPricePredictor:
    def __init__(self):

        try:
            logger.info(
                "Loading model artifacts"
            )

            self.model = joblib.load(
                "artifacts/models/"
                "best_flight_price_model.pkl"
            )

            self.preprocessor = joblib.load(
                "artifacts/models/"
                "preprocessor.pkl"
            )

            logger.info(
                "Artifacts loaded successfully"
            )

        except Exception as e:
            raise CustomException(e, sys)

    def predict(
        self,
        input_dataframe: pd.DataFrame
    ):

        try:
            logger.info(
                "Starting prediction pipeline"
            )

            transformed_data = (
                self.preprocessor.transform(
                    input_dataframe
                )
            )

            prediction = self.model.predict(
                transformed_data
            )

            logger.info(
                f"Prediction completed: "
                f"{prediction[0]}"
            )

            return prediction[0]

        except Exception as e:
            raise CustomException(e, sys)