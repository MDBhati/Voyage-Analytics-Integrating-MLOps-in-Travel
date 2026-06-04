from src.data.ingestion import DataIngestion
from src.data.validation import DataValidation

from src.data.schema import (
    FLIGHTS_SCHEMA
)

ingestion = DataIngestion()
validation = DataValidation()

flights_df = ingestion.load_flights_data()

validation.validate_columns(
    flights_df,
    FLIGHTS_SCHEMA
)

validation.validate_dtypes(
    flights_df,
    FLIGHTS_SCHEMA
)

validation.check_missing_values(
    flights_df
)

validation.check_duplicates(
    flights_df
)

print("Validation completed successfully")