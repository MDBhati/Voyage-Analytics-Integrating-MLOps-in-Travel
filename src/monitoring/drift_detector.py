import pandas as pd


class DriftDetector:

    def __init__(self):

        self.training_stats = {

            "distance_mean": 1500,

            "distance_std": 800,

            "time_mean": 5,

            "time_std": 2
        }

    def detect_distance_drift(
        self,
        distance
    ):

        mean = self.training_stats[
            "distance_mean"
        ]

        std = self.training_stats[
            "distance_std"
        ]

        z_score = abs(
            (distance - mean) / std
        )

        return z_score > 3