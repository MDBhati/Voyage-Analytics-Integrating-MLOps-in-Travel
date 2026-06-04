import requests

API_URL = "http://localhost:8000"


def predict_flight_price(payload):
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Prediction API is not reachable. Start it with: "
            "uvicorn src.api.app:app --reload --port 8000"
        ) from exc
    except requests.exceptions.HTTPError as exc:
        detail = exc.response.text if exc.response is not None else str(exc)
        raise RuntimeError(f"Prediction API error: {detail}") from exc
