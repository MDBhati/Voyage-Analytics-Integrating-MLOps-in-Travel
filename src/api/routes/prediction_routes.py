from fastapi import APIRouter, HTTPException

from src.api.schemas.prediction_schema import (
    FlightPredictionRequest,
)
from src.api.services.prediction_service import predict_flight_price
from src.utils.exception import CustomException

router = APIRouter()


@router.post(
    "/predict",
    summary="Predict flight price",
    response_description="Estimated ticket price in USD",
)
def predict(request: FlightPredictionRequest):
    """
    Estimate flight ticket price from route and trip features.

    The model uses trained artifacts in `artifacts/models/` (regression model
    + preprocessor). Inputs must match training schema: origin, destination,
    flight class, agency, duration (hours), and distance (km).
    """
    try:
        prediction = predict_flight_price(request)
    except (CustomException, FileNotFoundError) as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Flight price model is not available. "
                "Train it with: python run_training_pipeline.py"
            ),
        ) from exc

    return {
        "predicted_price": round(float(prediction), 2),
        "currency": "USD",
        "inputs": request.model_dump(),
    }
