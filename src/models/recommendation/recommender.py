import joblib


class HotelRecommender:

    def __init__(self):

        self.engine = joblib.load(
            "artifacts/models/hotel_recommender.pkl"
        )

    def recommend(
        self,
        hotel_name
    ):

        return self.engine.recommend_hotels(
            hotel_name
        )