import sys
import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException
from src.data.schema import (
    FLIGHTS_SCHEMA,
    HOTELS_SCHEMA,
    USERS_SCHEMA
)

class DataValidation:

    def validate_columns(
        self,
        dataframe: pd.DataFrame,
        required_schema: dict
    ):

        try:
            logger.info("Validating dataset columns")

            dataframe_columns = set(dataframe.columns)
            required_columns = set(required_schema.keys())

            missing_columns = required_columns - dataframe_columns

            if missing_columns:

                raise ValueError(
                    f"Missing columns: {missing_columns}"
                )

            logger.info("Column validation successful")

            return True

        except Exception as e:
            logger.error("Column validation failed")
            raise CustomException(e, sys)

    def validate_dtypes(
        self,
        dataframe: pd.DataFrame,
        required_schema: dict
    ):

        try:
            logger.info("Validating datatypes")

            for column, expected_dtype in required_schema.items():

                actual_dtype = str(dataframe[column].dtype)

                if actual_dtype != expected_dtype:

                    raise ValueError(
                        f"Datatype mismatch in column "
                        f"{column}. "
                        f"Expected: {expected_dtype}, "
                        f"Found: {actual_dtype}"
                    )

            logger.info("Datatype validation successful")

            return True

        except Exception as e:
            logger.error("Datatype validation failed")
            raise CustomException(e, sys)

    def check_missing_values(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info("Checking missing values")

            missing_values = dataframe.isnull().sum()

            logger.info(
                f"Missing values summary: "
                f"{missing_values.to_dict()}"
            )

            return missing_values

        except Exception as e:
            logger.error("Missing value check failed")
            raise CustomException(e, sys)

    def check_duplicates(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info("Checking duplicate rows")

            duplicate_count = dataframe.duplicated().sum()

            logger.info(
                f"Duplicate rows found: {duplicate_count}"
            )

            return duplicate_count

        except Exception as e:
            logger.error("Duplicate check failed")
            raise CustomException(e, sys)