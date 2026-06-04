import pandas as pd

from src.models.regression.predict import (
    FlightPricePredictor
)

predictor = FlightPricePredictor()

sample_input = pd.DataFrame({
    "from": ["London"],
    "to": ["Paris"],
    "flightType": ["Economy"],
    "agency": ["Air France"],
    "time": [2.5],
    "distance": [350]
})

prediction = predictor.predict(
    sample_input
)

print(
    f"Predicted Flight Price: "
    f"{prediction}"
)