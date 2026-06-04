# Voyage Analytics — Short Documentation

A compact MLOps platform for travel data: **flight price prediction**, **traveler
gender classification**, and **hotel recommendations**. The project ships a
FastAPI service, a Streamlit dashboard, training pipelines tracked by MLflow,
data versioning with DVC, an Airflow DAG, Docker packaging, and Prometheus
monitoring.

---

## 1. What this project does

| Capability | Type | Data source | Entry point |
|---|---|---|---|
| Flight price prediction | Regression | `data/raw/flights.csv` | `python run_training_pipeline.py` |
| Gender classification | Classification | `data/raw/users.csv` | `python run_gender_classification_training.py` |
| Hotel recommendations | Content-based similarity | `data/raw/hotels.csv` | `python run_recommendation_training.py` |

All trained artifacts are written to `artifacts/models/` and metrics to
`artifacts/metrics/`. Both the API and the Streamlit app load directly from
these artifacts.

---

## 2. Repository layout (actual)

```
voyage-analytics/
├── src/
│   ├── api/                  FastAPI app, routes, schemas, services, templates
│   ├── data/                 ingestion, validation, preprocessing, schema, bootstrap
│   ├── features/             feature_engineering.py
│   ├── models/
│   │   ├── regression/       flight price train / predict / evaluate
│   │   ├── classification/   gender train / predict / evaluate / preprocess
│   │   └── recommendation/   trainer, recommender, similarity_engine
│   ├── pipelines/            training_pipeline.py, inference_pipeline.py
│   ├── monitoring/           drift_detector, metrics, logger
│   ├── utils/                logger, exception, common helpers
│   └── visualization/
│
├── streamlit_app/            multi-page dashboard (app.py + pages/)
├── notebooks/eda/            EDA notebooks for each dataset
├── airflow/dags/             training_dag.py (daily flight-price training)
├── kubernetes/               deployment.yaml, service.yaml, hpa.yaml
├── configs/paths.yaml        dataset paths
├── data/raw/                 flights.csv, hotels.csv, users.csv (+ .dvc pointers)
├── artifacts/                models/, metrics/, predictions/, reports/
├── tests/                    unit, integration, api, models, pipelines
├── docs/                     this folder
├── .github/workflows/        mlops_ci.yaml (lint, train, build image)
├── Dockerfile                FastAPI container image
├── docker-compose.monitoring.yml   Prometheus + Grafana
├── dvc.yaml / dvc.lock       training_pipeline DVC stage
├── run_training_pipeline.py             flight price trainer
├── run_gender_classification_training.py gender classifier trainer
└── run_recommendation_training.py       hotel recommender trainer
```

---

## 3. Architecture at a glance

```
        data/raw/*.csv  ──►  src/data (ingest → validate → preprocess)
                                       │
                                       ▼
                            src/features (engineering)
                                       │
                ┌──────────────────────┼──────────────────────┐
                ▼                      ▼                      ▼
        regression.train       classification.train    recommendation.trainer
                │                      │                      │
                └────────► artifacts/models/  ◄────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                              ▼
        src/api (FastAPI)                              streamlit_app (UI)
        /predict, /classify/gender                     flight / gender / hotels / analytics
                │
                ▼
        Prometheus  ──►  Grafana  (docker-compose.monitoring.yml)
```

Cross-cutting:
- **MLflow** — experiments + runs (`mlruns/`, `mlflow.db`)
- **DVC** — data + pipeline versioning (`dvc.yaml`, `data/raw/*.dvc`)
- **Airflow** — `flight_price_training_pipeline` DAG runs daily
- **GitHub Actions** — `.github/workflows/mlops_ci.yaml` runs training and
  builds the Docker image on every push to `main`

---

## 4. Setup

Requires Python 3.11.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/ensure_raw_data.py
```

Core dependencies (see `requirements.txt`): pandas, scikit-learn, FastAPI,
Streamlit, MLflow, DVC, Plotly, Prometheus instrumentator.

---

## 5. Train the models

```bash
python run_training_pipeline.py                  # flight price regression
python run_gender_classification_training.py     # gender classifier
python run_recommendation_training.py            # hotel recommender
```

Each script writes models to `artifacts/models/` and JSON metrics to
`artifacts/metrics/`. The flight-price pipeline is also wrapped as a DVC stage:

```bash
dvc repro
```

---

## 6. Run the services

### FastAPI

```bash
uvicorn src.api.app:app --reload --port 8000
```

| Endpoint | Method | Purpose |
|---|---|---|
| `/`, `/health` | GET | service metadata + liveness |
| `/docs` | GET | Swagger UI |
| `/metrics` | GET | Prometheus metrics |
| `/predict` | POST | flight price prediction |
| `/classify/gender` | POST | traveler gender classification |

Sample request:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"from_location":"Sao Paulo","to_location":"Rio de Janeiro","flightType":"economic","agency":"Rainbow","time":1.5,"distance":420.0}'
```

### Streamlit dashboard

```bash
streamlit run streamlit_app/app.py
```

Pages: Flight Prediction, Hotel Recommendations, Gender Classification,
Analytics Dashboard. The UI loads models directly from `artifacts/models/`
(no API call required).

### Monitoring

```bash
docker compose -f docker-compose.monitoring.yml up -d
# Prometheus → http://localhost:9090
# Grafana    → http://localhost:3000
```

### Docker (API)

```bash
docker build -t voyage-analytics-api .
docker run -p 8000:8000 voyage-analytics-api
```

### Airflow

The DAG `flight_price_training_pipeline` (`airflow/dags/training_dag.py`)
runs `run_training_pipeline.py` daily. Mount the repo at `/opt/airflow/project`.

### Kubernetes

Manifests in `kubernetes/` deploy the API with a `Service` and `HorizontalPodAutoscaler`:

```bash
kubectl apply -f kubernetes/
```

---

## 7. Testing

Pytest suites live in `tests/` (unit, integration, api, models, pipelines)
with top-level smoke tests for ingestion, validation, preprocessing, feature
engineering, training, and prediction.

```bash
pytest
```

---

## 8. CI/CD

`.github/workflows/mlops_ci.yaml` runs on push / PR to `main`:

1. Install dependencies
2. Ensure raw datasets exist
3. Reset MLflow store
4. Run training pipelines (flight + gender)
5. Validate that `src.api.app` imports cleanly
6. Build the API Docker image

---

## 9. Key configuration

- `configs/paths.yaml` — paths to raw datasets
- `dvc.yaml` — pipeline stage `training_pipeline` with deps/outs/metrics
- `Dockerfile` — Python 3.11-slim, exposes port 8000, runs uvicorn
- `requirements.txt` — pinned versions of all runtime libraries

---

## 10. Where to look next

- **Exploratory analysis:** `notebooks/eda/*.ipynb`
- **Model code:** `src/models/{regression,classification,recommendation}/`
- **Pipelines:** `src/pipelines/training_pipeline.py`, `inference_pipeline.py`
- **API surface:** `src/api/app.py` + `src/api/routes/`
- **Dashboard:** `streamlit_app/app.py` + `streamlit_app/pages/`
