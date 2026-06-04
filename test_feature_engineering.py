from src.data.ingestion import DataIngestion
from src.data.validation import DataValidation
from src.data.preprocessing import DataPreprocessor

from src.features.feature_engineering import (
    FeatureEngineer
)

from src.data.schema import FLIGHTS_SCHEMA

ingestion = DataIngestion()
validation = DataValidation()
preprocessor = DataPreprocessor()
feature_engineer = FeatureEngineer()

flights_df = ingestion.load_flights_data()

validation.validate_columns(
    flights_df,
    FLIGHTS_SCHEMA
)

validation.validate_dtypes(
    flights_df,
    FLIGHTS_SCHEMA
)

flights_df = preprocessor.process_dates(
    flights_df
)

flights_df = (
    feature_engineer.engineer_flight_features(
        flights_df
    )
)

print(
    flights_df[
        [
            "route",
            "route_frequency",
            "agency_avg_price",
            "is_weekend",
            "user_trip_count"
        ]
    ].head()
)