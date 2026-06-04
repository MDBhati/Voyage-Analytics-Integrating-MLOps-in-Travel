import sys
import joblib
import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException


class GenderClassifier:

    def __init__(self):
        try:
            logger.info("Loading gender classification artifacts")

            self.model = joblib.load(
                "artifacts/models/gender_classifier.pkl"
            )
            self.preprocessor = joblib.load(
                "artifacts/models/gender_classifier_preprocessor.pkl"
            )

            logger.info("Gender classification artifacts loaded")

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, input_dataframe: pd.DataFrame):
        try:
            transformed = self.preprocessor.transform(input_dataframe)
            prediction = self.model.predict(transformed)[0]
            probabilities = None

            if hasattr(self.model, "predict_proba"):
                proba = self.model.predict_proba(transformed)[0]
                probabilities = {
                    label: round(float(score), 4)
                    for label, score in zip(self.model.classes_, proba)
                }

            return prediction, probabilities

        except Exception as e:
            raise CustomException(e, sys)
