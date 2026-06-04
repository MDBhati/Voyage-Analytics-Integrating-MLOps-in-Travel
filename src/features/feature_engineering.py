import sys
import pandas as pd

from src.utils.logger import logger
from src.utils.exception import CustomException

class FeatureEngineer:

    def create_route_feature(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info(
                "Creating route feature"
            )

            dataframe["route"] = (
                dataframe["from"]
                + "_"
                + dataframe["to"]
            )

            return dataframe

        except Exception as e:
            raise CustomException(e, sys)

    def create_route_frequency_feature(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info(
                "Creating route frequency feature"
            )

            route_counts = (
                dataframe["route"]
                .value_counts()
                .to_dict()
            )

            dataframe["route_frequency"] = (
                dataframe["route"]
                .map(route_counts)
            )

            return dataframe

        except Exception as e:
            raise CustomException(e, sys)

    def create_agency_price_feature(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info(
                "Creating agency average pricing feature"
            )

            agency_avg_price = (
                dataframe
                .groupby("agency")["price"]
                .mean()
                .to_dict()
            )

            dataframe["agency_avg_price"] = (
                dataframe["agency"]
                .map(agency_avg_price)
            )

            return dataframe

        except Exception as e:
            raise CustomException(e, sys)
    
    def create_weekend_feature(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info(
                "Creating weekend travel feature"
            )

            dataframe["is_weekend"] = (
                dataframe["weekday"]
                >= 5
            ).astype(int)

            return dataframe

        except Exception as e:
            raise CustomException(e, sys)

    def create_user_travel_frequency(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info(
                "Creating user travel frequency feature"
            )

            user_trip_counts = (
                dataframe["userCode"]
                .value_counts()
                .to_dict()
            )

            dataframe["user_trip_count"] = (
                dataframe["userCode"]
                .map(user_trip_counts)
            )

            return dataframe

        except Exception as e:
            raise CustomException(e, sys)

    def engineer_flight_features(
        self,
        dataframe: pd.DataFrame
    ):

        try:
            logger.info(
                "Starting feature engineering"
            )

            dataframe = self.create_route_feature(
                dataframe
            )

            dataframe = (
                self.create_route_frequency_feature(
                    dataframe
                )
            )

            dataframe = (
                self.create_agency_price_feature(
                    dataframe
                )
            )

            dataframe = self.create_weekend_feature(
                dataframe
            )

            dataframe = (
                self.create_user_travel_frequency(
                    dataframe
                )
            )

            logger.info(
                "Feature engineering completed"
            )

            return dataframe

        except Exception as e:
            raise CustomException(e, sys)