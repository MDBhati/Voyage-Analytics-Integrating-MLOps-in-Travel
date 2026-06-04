from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from src.api.templates.loader import load_template

router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    return load_template("home.html")


@router.get("/about", tags=["System"])
def about():
    return {
        "name": "Voyage Analytics API",
        "version": "1.0.0",
        "objective": (
            "Deliver travel analytics and ML inference as a reproducible, "
            "monitorable service integrated with the Voyage Analytics MLOps stack."
        ),
        "capabilities": [
            "Flight price prediction (POST /predict)",
            "Gender classification (POST /classify/gender)",
            "Prometheus metrics (/metrics)",
            "OpenAPI documentation (/docs, /redoc)",
            "Companion Streamlit dashboard for analytics and artifact-based UI",
        ],
        "datasets": [
            "Flights — routes, agencies, duration, distance, price",
            "Hotels — bookings, places, names, pricing",
            "Users — traveler profiles for classification workflows",
        ],
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "metrics": "/metrics",
        },
    }


@router.get("/health", tags=["System"])
def health():
    return JSONResponse(
        content={"status": "healthy", "service": "voyage-analytics-api"},
        status_code=200,
    )
