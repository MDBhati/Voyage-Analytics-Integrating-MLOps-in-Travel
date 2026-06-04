import joblib

from src.models.recommendation.similarity_engine import (
    HotelSimilarityEngine
)

class RecommendationTrainer:

    def train(
        self,
        hotels_df
    ):

        engine = HotelSimilarityEngine()

        engine.fit(
            hotels_df
        )

        joblib.dump(
            engine,
            "artifacts/models/hotel_recommender.pkl"
        )
    