import pandas as pd
import yaml
import sys

from src.utils.logger import logger
from src.utils.exception import CustomException


class DataIngestion:
    def __init__(self, config_path="configs/paths.yaml"):

        with open(config_path, "r") as file:
            self.paths = yaml.safe_load(file)

    def load_flights_data(self):

        try:
            logger.info("Loading flights dataset")

            flights_df = pd.read_csv(
                self.paths["data_paths"]["flights_data"]
            )

            logger.info(
                f"Flights dataset loaded successfully "
                f"with shape {flights_df.shape}"
            )

            return flights_df

        except Exception as e:
            logger.error("Failed to load flights dataset")
            raise CustomException(e, sys)

    def load_hotels_data(self):

        try:
            logger.info("Loading hotels dataset")

            hotels_df = pd.read_csv(
                self.paths["data_paths"]["hotels_data"]
            )

            logger.info(
                f"Hotels dataset loaded successfully "
                f"with shape {hotels_df.shape}"
            )

            return hotels_df

        except Exception as e:
            logger.error("Failed to load hotels dataset")
            raise CustomException(e, sys)

    def load_users_data(self):

        try:
            logger.info("Loading users dataset")

            users_df = pd.read_csv(
                self.paths["data_paths"]["users_data"]
            )

            logger.info(
                f"Users dataset loaded successfully "
                f"with shape {users_df.shape}"
            )

            return users_df

        except Exception as e:
            logger.error("Failed to load users dataset")
            raise CustomException(e, sys)