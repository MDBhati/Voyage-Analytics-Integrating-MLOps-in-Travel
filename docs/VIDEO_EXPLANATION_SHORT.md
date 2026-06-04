# Voyage Analytics — 10-Minute Video Script (Trimmed)

A tighter version of `docs/VIDEO_EXPLANATION.md` for a 10-minute walkthrough.
Same 8-section structure, condensed to the essentials. Use this when you
need to fit a shorter slot or when the rubric rewards conciseness.

> **Stack note:** project uses **FastAPI** (not Flask) and **GitHub Actions**
> (not Jenkins). They serve the same role; the script uses the real stack.

---

## 1. Introduction (1 min)

**Show:** project root in IDE.

> "I built **Voyage Analytics** — an end-to-end MLOps platform in the
> travel domain that ships three production ML services from one codebase:
> **flight price prediction** (regression), **traveler gender
> classification**, and **hotel recommendations**. The stack is
> production-shaped: Python, FastAPI, Streamlit, MLflow, DVC, Airflow,
> Docker, Kubernetes, Prometheus, and GitHub Actions for CI/CD. The
> goal of this walkthrough is the **end-to-end system**, not just a
> trained model."

---

## 2. Problem Understanding (1 min)

**Show:** a notebook → then `src/api/app.py`.

> "Travel pricing has strong statistical signal but no clean rule, so a
> regression model captures it better than heuristics. Recommendations
> rank a few hotels out of thousands. Profile classification feeds
> personalization. But none of that ships from a notebook — a notebook
> can't serve mobile traffic, can't retrain on schedule, can't roll
> back. So this project treats ML as four tasks that must run
> reliably: **predict, classify, recommend, automate.** A notebook
> proves an idea works once; an MLOps pipeline guarantees it keeps
> working."

---

## 3. Data & Use-Case Mapping (1 min)

**Show:** the three CSVs.

> "Three datasets — `users.csv`, `flights.csv`, `hotels.csv` — connected by
> two foreign keys. **`userCode`** joins traveler demographics onto any
> booking. **`travelCode`** links the flight and hotel from the same trip.
> That's how the three models become one product: the same `userCode`
> flows through gender classification for personalization, the regressor
> for price expectations, and the recommender for the next stay."

---

## 4. Model Development & Serving (1.5 min)

**Show:** `src/pipelines/training_pipeline.py` → `src/api/routes/prediction_routes.py`.

> "All three models share the same upstream stages — ingestion, schema
> validation, date processing, feature engineering, preprocessing —
> orchestrated by `TrainingPipeline`. Feature engineering is route-aware
> for flights and TF-IDF text features for hotels. The critical detail:
> the `ColumnTransformer` is **persisted with the model**, so training
> and serving use the *same* transformations — no train/serve skew.
>
> The regressor and classifier are exposed via FastAPI:
> `POST /predict` and `POST /classify/gender`. Pydantic validates the
> JSON, the service loads the trained pipeline from
> `artifacts/models/`, runs `predict`, and returns the result with the
> inputs echoed back. If the artifact is missing, the API returns
> `503` with the exact training command — the failure mode is
> operationally obvious."

---

## 5. MLOps Pipeline & Deployment (1.5 min)

**Show:** `Dockerfile` · `kubernetes/` · `airflow/dags/training_dag.py` · `mlruns/`.

> "Six tools, six clear roles:
>
> - **Docker** — `python:3.11-slim` image running `uvicorn` on port 8000.
> - **Kubernetes** — `deployment.yaml`, `service.yaml`, and a HPA in
>   `hpa.yaml` for traffic-based scaling.
> - **GitHub Actions** — CI/CD: install, train both models, validate
>   the API imports, build the Docker image, all on every push to
>   `main`.
> - **Airflow** — the `flight_price_training_pipeline` DAG retrains
>   daily.
> - **MLflow** — every run logs params, metrics, and the artifact to
>   `mlruns/`; the registry handles version promotion.
> - **DVC** — `dvc.yaml` declares the training stage with explicit
>   deps and outs, so `dvc repro` re-runs only what's stale.
>
> Code in Git · Data in DVC · Experiments in MLflow · Image in
> Registry · Runtime in K8s · Schedule in Airflow."

---

## 6. Recommender, UI & Monitoring (1 min)

**Show:** `streamlit_app/app.py` running · `docker-compose.monitoring.yml`.

> "The recommender is content-based — TF-IDF over hotel `name` and
> `place`, cosine similarity, top-K. Simple, no cold-start, strong
> baseline. The Streamlit dashboard has four pages — flight prediction,
> hotel recommendations, gender classification, and an analytics
> dashboard — all loading models directly from `artifacts/models/`,
> so the UI works even when the API is down. Monitoring is the
> Prometheus instrumentator on FastAPI exposing `/metrics`, with
> Grafana dashboards via `docker-compose.monitoring.yml`. Drift
> detection in `src/monitoring/drift_detector.py` is the trigger for
> retraining."

---

## 7. Reliability & Optimization (1 min)

**Show:** `dvc.yaml` · `tests/`.

> "The hard parts weren't the models. **Three schemas** were kept in
> sync via `src/data/schema.py` and a fast-failing validation step.
> **API design** uses Pydantic for typed contracts and a `503` with the
> exact training command on missing artifacts. **Deployment** complexity
> is contained in one Docker image plus Kubernetes manifests.
> **Path drift** between Airflow, DVC, and MLflow is solved by
> centralizing in `configs/paths.yaml`. Reliability comes from three
> things: **Git for code, DVC for data, MLflow for models** — every run
> reproducible end-to-end."

---

## 8. Learnings & Future Improvements (1 min)

**Show:** project root.

> "The real lesson is that training is maybe 20% of production ML.
> Reproducibility, schemas, observability, and automation are the other
> 80%. Next steps are already shaped by the architecture:
> **drift-triggered auto-retraining**, **OAuth2 on the API**,
> a **hybrid recommender** combining content with collaborative
> filtering on `userCode`/`travelCode` history, and **cloud-managed
> MLflow** (S3 + Postgres) plus **managed Airflow** (MWAA / Composer).
> None of these require rewriting the system — only extending it."

---

## Q&A Cheat Sheet (kept verbatim from full script)

**1. Productionize real-time pricing?** Freeze the preprocessing pipeline
with the model · expose with FastAPI + Pydantic · deploy as a Docker
image on K8s with HPA · instrument with Prometheus, drift detection,
and an MLflow registry for one-command rollback.

**2. Why Docker + Kubernetes?** Docker = reproducible runtime.
Kubernetes = replicas, auto-scaling via HPA, rolling updates,
self-healing pods, stable service endpoint. Same image on laptop, CI,
and prod.

**3. How does MLflow help with versions?** Three things — Tracking
(params/metrics/artifacts per run), Models (uniform load API), Registry
(stages: Staging → Production). Rollback is one config change.

**4. How would you handle retraining?** Two triggers, one DAG. Time
trigger = daily Airflow. Event trigger = drift detector. The DAG runs
the same `TrainingPipeline`, logs to MLflow, and only promotes if the
new run beats Production. Pods pick up the new model on next restart.

**5. How would you scale for a large platform?** Five layers — serving
(HPA + CDN + per-model pods), data (warehouse + Spark/dbt), feature
store (Feast), training (distributed: Ray / SageMaker), operations
(managed MLflow + MWAA + PagerDuty). Code structure unchanged — each
component swapped behind the same interface.
