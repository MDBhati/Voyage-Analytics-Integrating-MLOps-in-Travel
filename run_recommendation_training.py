import pandas as pd

from src.models.recommendation.trainer import (
    RecommendationTrainer
)

hotels_df = pd.read_csv(
    "data/raw/hotels.csv"
)

trainer = RecommendationTrainer()

trainer.train(
    hotels_df
)

print(
    "Recommendation model trained"
)