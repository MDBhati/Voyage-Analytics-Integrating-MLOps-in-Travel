import sys

from src.utils.logger import logger
from src.utils.exception import CustomException

from src.data.ingestion import DataIngestion
from src.data.validation import DataValidation
from src.data.preprocessing import DataPreprocessor

from src.features.feature_engineering import (
    FeatureEngineer
)

from src.models.regression.train import (
    FlightPriceTrainer
)

from src.data.schema import (
    FLIGHTS_SCHEMA
)

class TrainingPipeline:
    def __init__(self):

        self.ingestion = DataIngestion()

        self.validation = DataValidation()

        self.preprocessor = DataPreprocessor()

        self.feature_engineer = FeatureEngineer()

        self.trainer = FlightPriceTrainer()
    
    def run_pipeline(self):
        try:

            logger.info(
                "Starting training pipeline"
            )

            # =========================
            # DATA INGESTION
            # =========================

            flights_df = (
                self.ingestion.load_flights_data()
            )

            logger.info(
                "Data ingestion completed"
            )

            # =========================
            # VALIDATION
            # =========================

            self.validation.validate_columns(
                flights_df,
                FLIGHTS_SCHEMA
            )

            self.validation.validate_dtypes(
                flights_df,
                FLIGHTS_SCHEMA
            )

            logger.info(
                "Validation completed"
            )

            # =========================
            # DATE PROCESSING
            # =========================

            flights_df = (
                self.preprocessor.process_dates(
                    flights_df
                )
            )

            logger.info(
                "Date processing completed"
            )

            # =========================
            # FEATURE ENGINEERING
            # =========================

            flights_df = (
                self.feature_engineer
                .engineer_flight_features(
                    flights_df
                )
            )

            logger.info(
                "Feature engineering completed"
            )

            # =========================
            # PREPROCESSING
            # =========================

            X_transformed, y, preprocessor = (
                self.preprocessor
                .preprocess_flights_data(
                    flights_df
                )
            )

            logger.info(
                "Preprocessing completed"
            )

            # =========================
            # MODEL TRAINING
            # =========================

            report = self.trainer.train_models(
                X_transformed,
                y,
                preprocessor
            )

            logger.info(
                "Model training completed"
            )

            logger.info(
                f"Training report: {report}"
            )

            return report

        except Exception as e:

            logger.error(
                "Training pipeline failed"
            )

            raise CustomException(e, sys)