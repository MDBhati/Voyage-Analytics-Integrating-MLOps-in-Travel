from functools import lru_cache

import pandas as pd

from src.monitoring.logger import prediction_logger
from src.monitoring.drift_detector import DriftDetector
from src.models.regression.predict import FlightPricePredictor


@lru_cache(maxsize=1)
def _get_predictor():
    return FlightPricePredictor()


@lru_cache(maxsize=1)
def _get_drift_detector():
    return DriftDetector()


def predict_flight_price(request):
    input_df = pd.DataFrame(
        {
            "from": [request.from_location],
            "to": [request.to_location],
            "flightType": [request.flightType],
            "agency": [request.agency],
            "time": [request.time],
            "distance": [request.distance],
        }
    )

    drift_detector = _get_drift_detector()

    if drift_detector.detect_distance_drift(request.distance):
        prediction_logger.warning(
            f"Potential distance drift detected: {request.distance}"
        )

    prediction = _get_predictor().predict(input_df)

    prediction_logger.info(
        f"""
        Input: {input_df.to_dict()}
        Prediction: {prediction}
        """
    )

    return prediction
