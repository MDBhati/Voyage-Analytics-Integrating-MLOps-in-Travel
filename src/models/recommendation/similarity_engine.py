import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class HotelSimilarityEngine:

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.similarity_matrix = None
        self.hotel_names = None
        self.hotels_df = None  # legacy artifacts only

    def prepare_features(self, hotels_df):
        hotels_df = hotels_df.copy()
        hotels_df["combined_features"] = (
            hotels_df["place"].astype(str) + " " + hotels_df["name"].astype(str)
        )
        return hotels_df

    def fit(self, hotels_df):
        unique_hotels = (
            hotels_df.drop_duplicates(subset="name").reset_index(drop=True)
        )
        unique_hotels = self.prepare_features(unique_hotels)

        self.hotel_names = unique_hotels["name"].tolist()

        feature_matrix = self.vectorizer.fit_transform(
            unique_hotels["combined_features"]
        )
        self.similarity_matrix = cosine_similarity(feature_matrix)

        # Inference only needs names + matrix; drop heavy training objects.
        self.vectorizer = None
        self.hotels_df = None

    def recommend_hotels(self, hotel_name, top_n=5):
        if self.hotel_names is not None:
            hotel_index = self.hotel_names.index(hotel_name)
            names = self.hotel_names
        else:
            # Backward compatibility with old large artifacts.
            hotel_index = self.hotels_df[
                self.hotels_df["name"] == hotel_name
            ].index[0]
            names = self.hotels_df["name"].tolist()

        scores = self.similarity_matrix[hotel_index]
        ranked_indices = np.argsort(scores)[::-1]

        recommendations = []
        seen = {hotel_name}
        for index in ranked_indices:
            name = names[index]
            if name in seen:
                continue
            seen.add(name)
            recommendations.append(name)
            if len(recommendations) >= top_n:
                break

        return recommendations
