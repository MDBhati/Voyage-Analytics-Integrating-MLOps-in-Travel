from src.data.ingestion import DataIngestion
from src.data.validation import DataValidation
from src.data.preprocessing import DataPreprocessor

from src.data.schema import FLIGHTS_SCHEMA

ingestion = DataIngestion()
validation = DataValidation()
preprocessor = DataPreprocessor()

flights_df = ingestion.load_flights_data()

validation.validate_columns(
    flights_df,
    FLIGHTS_SCHEMA
)

validation.validate_dtypes(
    flights_df,
    FLIGHTS_SCHEMA
)

X_transformed, y, processor = (
    preprocessor.preprocess_flights_data(
        flights_df
    )
)

print(X_transformed.shape)
print(y.head())