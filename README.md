# Voyage Analytics - Travel Data Analytics Platform

A comprehensive MLOps project for travel analytics,featuring gender classification, flight price prediction and hotel recommendations.

## Project Structure

voyage-analytics/
```
│
├── README.md
├── requirements.txt
├── pyproject.toml
├── setup.py
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── LICENSE
│
├── .github/
│   └── workflows/
│       ├── ci.yaml
│       ├── cd.yaml
│       ├── model-training.yaml
│       └── lint-test.yaml
│
├── configs/
│   ├── config.yaml
│   ├── model_config.yaml
│   ├── paths.yaml
│   └── logging.yaml
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── external/
│   └── feature_store/
│
├── dvc.yaml
├── dvc.lock
├── .dvc/
│   ├── config
│   ├── .gitignore
│   └── tmp/
│
├── artifacts/
│   ├── models/
│   ├── metrics/
│   ├── predictions/
│   └── reports/
│
├── notebooks/
│   ├── eda/
│   ├── experiments/
│   ├── feature_engineering/
│   └── model_analysis/
│
├── src/
│   │
│   ├── data/
│   │   ├── ingestion.py
│   │   ├── validation.py
│   │   ├── preprocessing.py
│   │   ├── data_split.py
│   │   └── schema.py
│   │
│   ├── features/
│   │   ├── feature_engineering.py
│   │   ├── feature_selection.py
│   │   └── feature_store.py
│   │
│   ├── models/
│   │   ├── regression/
│   │   │   ├── train.py
│   │   │   ├── predict.py
│   │   │   └── evaluate.py
│   │   │
│   │   ├── classification/
│   │   │   ├── train.py
│   │   │   ├── predict.py
│   │   │   └── evaluate.py
│   │   │
│   │   ├── recommendation/
│   │   │   ├── train.py
│   │   │   ├── recommend.py
│   │   │   └── evaluate.py
│   │   │
│   │   ├── registry/
│   │   │   └── model_registry.py
│   │   │
│   │   └── tracking/
│   │       └── mlflow_tracker.py
│   │
│   ├── pipelines/
│   │   ├── training_pipeline.py
│   │   ├── inference_pipeline.py
│   │   ├── batch_pipeline.py
│   │   └── retraining_pipeline.py
│   │
│   ├── api/
│   │   ├── main.py
│   │   ├── dependencies.py
│   │   │
│   │   ├── routes/
│   │   │   ├── regression_routes.py
│   │   │   ├── classification_routes.py
│   │   │   └── recommendation_routes.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── request_schema.py
│   │   │   └── response_schema.py
│   │   │
│   │   └── services/
│   │       ├── prediction_service.py
│   │       └── recommendation_service.py
│   │
│   ├── monitoring/
│   │   ├── drift_detection.py
│   │   ├── model_monitoring.py
│   │   ├── performance_monitor.py
│   │   └── alerting.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── exception.py
│   │   ├── helpers.py
│   │   ├── common.py
│   │   └── constants.py
│   │
│   └── visualization/
│       ├── plots.py
│       └── dashboards.py
│
├── mlruns/
│
├── airflow/
│   ├── dags/
│   │   ├── training_dag.py
│   │   ├── batch_prediction_dag.py
│   │   └── retraining_dag.py
│   │
│   ├── plugins/
│   ├── logs/
│   └── requirements.txt
│
├── kubernetes/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── persistent-volume.yaml
│
├── streamlit_app/
│   ├── app.py
│   │
│   ├── pages/
│   │   ├── flight_prediction.py
│   │   ├── gender_classification.py
│   │   ├── hotel_recommendation.py
│   │   └── analytics_dashboard.py
│   │
│   ├── components/
│   └── assets/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   ├── pipelines/
│   └── models/
│
├── deployment/
│   ├── docker/
│   ├── kubernetes/
│   └── scripts/
│
├── docs/
│   ├── architecture/
│   ├── api_docs/
│   ├── diagrams/
│   ├── workflows/
│   └── ml_lifecycle/
│
├── logs/
│
├── experiments/
│
└── scripts/
    ├── setup_env.sh
    ├── train_model.sh
    ├── deploy.sh
    └── run_pipeline.sh
```

## Features

1. **Flight Price Prediction**
    - Regression model for flight price prediction
    - REST API for real-time predictions
    - Model verioning with MLFlow

2. **Gender Classification**
    - Classification model for user gender prediction
    - Model deployment and monitoring

3. **Hotel Recommendations**
    - Recommendation system for Hotels
    - Interactive Streamlit dashboard
    - User preference analysis

## MLOps Infrastruture

- **Containerization**: Docker for consistent environments
- **Orchestrations**: Kubernetes for scalable deployment
- **Workflow Automation**: Apache Airflow for data pipeline
- **CI/CD**: Github Actions for automated deployment
- **Model Tracking**: MLFlow for experiment tracking

## Setup and Installation


## Usage


## Contributing