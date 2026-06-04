from fastapi import APIRouter, HTTPException

from src.api.schemas.classification_schema import (
    GenderClassificationRequest,
)
from src.api.services.classification_service import predict_gender
from src.utils.exception import CustomException

router = APIRouter()


@router.post(
    "/classify/gender",
    summary="Classify traveler gender",
    response_description="Predicted gender label and class probabilities",
)
def classify_gender(request: GenderClassificationRequest):
    """
    Predict gender (male, female, or none) from traveler name, company, and age.

    Uses trained artifacts in `artifacts/models/gender_classifier.pkl`.
    """
    try:
        predicted_gender, probabilities = predict_gender(request)
    except (CustomException, FileNotFoundError) as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Gender classification model is not available. "
                "Train it with: python run_gender_classification_training.py"
            ),
        ) from exc

    return {
        "predicted_gender": predicted_gender,
        "probabilities": probabilities,
        "inputs": request.model_dump(),
    }
