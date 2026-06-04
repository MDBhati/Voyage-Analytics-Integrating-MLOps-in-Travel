import sys
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from src.utils.logger import logger
from src.utils.exception import CustomException


class DataPreprocessor:

    def __init__(self):

        self.categorical_columns = [
            "from",
            "to",
            "flightType",
            "agency"
        ]

        self.numerical_columns = [
            "time",
            "distance"
        ]

    def create_numerical_pipeline(self):

        try:
            logger.info(
                "Creating numerical preprocessing pipeline"
            )

            numerical_pipeline = Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(strategy="median")
                    ),

                    (
                        "scaler",
                        StandardScaler()
                    )
                ]
            )

            return numerical_pipeline

        except Exception as e:
            raise CustomException(e, sys)

    def create_categorical_pipeline(self):

        try:
            logger.info(
                "Creating categorical preprocessing pipeline"
            )

            categorical_pipeline = Pipeline(
                steps=[
                    (
                        "imputer",
                        SimpleImputer(strategy="most_frequent")
                    ),

                    (
                        "encoder",
                        OneHotEncoder(handle_unknown="ignore")
                    )
                ]
            )

            return categorical_pipeline

        except Exception as e:
            raise CustomException(e, sys)

    def create_preprocessor(self):

        try:
            logger.info(
                "Creating full preprocessing transformer"
            )

            numerical_pipeline = (
                self.create_numerical_pipeline()
            )

            categorical_pipeline = (
                self.create_categorical_pipeline()
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    (
                        "numerical_pipeline",
                        numerical_pipeline,
                        self.numerical_columns
                    ),

                    (
                        "categorical_pipeline",
                        categorical_pipeline,
                        self.categorical_columns
                    )
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def process_dates(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info("Processing date columns")

            dataframe["date"] = pd.to_datetime(
                dataframe["date"]
            )

            dataframe["year"] = (
                dataframe["date"].dt.year
            )

            dataframe["month"] = (
                dataframe["date"].dt.month
            )

            dataframe["day"] = (
                dataframe["date"].dt.day
            )

            dataframe["weekday"] = (
                dataframe["date"].dt.weekday
            )

            return dataframe

        except Exception as e:
            raise CustomException(e, sys)

    def preprocess_flights_data(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info(
                "Starting flights preprocessing"
            )

            dataframe = self.process_dates(
                dataframe
            )

            X = dataframe.drop(columns=["price"])

            y = dataframe["price"]

            preprocessor = self.create_preprocessor()

            X_transformed = preprocessor.fit_transform(X)

            logger.info(
                "Flights preprocessing completed"
            )

            return (
                X_transformed,
                y,
                preprocessor
            )

        except Exception as e:
            raise CustomException(e, sys)