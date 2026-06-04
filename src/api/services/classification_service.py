from functools import lru_cache

import pandas as pd

from src.models.classification.predict import GenderClassifier


@lru_cache(maxsize=1)
def _get_classifier():
    return GenderClassifier()


def predict_gender(request):
    input_df = pd.DataFrame(
        {
            "name": [request.name],
            "company": [request.company],
            "age": [request.age],
        }
    )

    predicted_gender, probabilities = _get_classifier().predict(input_df)

    return predicted_gender, probabilities
