from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routes.prediction_routes import router as prediction_router
from src.api.routes.classification_routes import router as classification_router
from src.api.routes.system_routes import router as system_router
from src.api.templates.loader import STATIC_DIR

from prometheus_fastapi_instrumentator import Instrumentator

API_DESCRIPTION = """
**Voyage Analytics** is an MLOps-ready travel analytics platform. It turns
flight and hotel booking data into actionable insights and machine learning
services.

### Objectives

- **Predict** flight prices from route, airline, duration, and distance features.
- **Classify** traveler gender from name, company, and age (male / female / none).
- **Recommend** similar hotels using content-based similarity on location and name.
- **Monitor** model serving with Prometheus metrics and drift-aware logging.
- **Operationalize** training and inference through pipelines, MLflow, Airflow, and containers.

### How to use this API

1. Open **Interactive docs** at [`/docs`](/docs) to try endpoints in the browser.
2. Call **`POST /predict`** with flight details to get a price estimate.
3. Call **`POST /classify/gender`** with traveler profile fields.
4. Use the **Streamlit dashboard** (`streamlit run streamlit_app/app.py`) for
   analytics charts and UI-driven predictions loaded from `artifacts/`.
"""

TAGS_METADATA = [
    {
        "name": "Prediction",
        "description": "Flight price inference using trained regression artifacts.",
    },
    {
        "name": "Classification",
        "description": "Traveler gender classification from user profile features.",
    },
    {
        "name": "System",
        "description": "Health checks and service metadata.",
    },
]

app = FastAPI(
    title="Voyage Analytics API",
    description=API_DESCRIPTION,
    version="1.0.0",
    contact={
        "name": "Voyage Analytics",
        "url": "https://github.com/your-org/voyage-analytics",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=TAGS_METADATA,
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

Instrumentator().instrument(app).expose(app)

app.include_router(system_router)
app.include_router(prediction_router, tags=["Prediction"])
app.include_router(classification_router, tags=["Classification"])
