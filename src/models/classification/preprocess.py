import sys
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer


def _name_to_strings(X):
    if hasattr(X, "values"):
        return X.values.ravel().astype(str)
    return X.ravel().astype(str)

from src.utils.logger import logger
from src.utils.exception import CustomException


class UserPreprocessor:

    def __init__(self):
        self.categorical_columns = ["company"]
        self.text_columns = ["name"]
        self.numerical_columns = ["age"]

    def create_preprocessor(self):
        try:
            text_pipeline = Pipeline(
                steps=[
                    ("to_str", FunctionTransformer(_name_to_strings)),
                    (
                        "tfidf",
                        TfidfVectorizer(
                            analyzer="word",
                            ngram_range=(1, 2),
                            max_features=500,
                        ),
                    ),
                ]
            )

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore")),
                ]
            )

            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("name_tfidf", text_pipeline, self.text_columns),
                    (
                        "company_encoder",
                        categorical_pipeline,
                        self.categorical_columns,
                    ),
                    (
                        "age_scaler",
                        numerical_pipeline,
                        self.numerical_columns,
                    ),
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def preprocess_users_data(self, dataframe: pd.DataFrame):
        try:
            logger.info("Starting users preprocessing for classification")

            X = dataframe[["name", "company", "age"]]
            y = dataframe["gender"]

            preprocessor = self.create_preprocessor()
            X_transformed = preprocessor.fit_transform(X)

            logger.info("Users preprocessing completed")

            return X_transformed, y, preprocessor

        except Exception as e:
            raise CustomException(e, sys)
