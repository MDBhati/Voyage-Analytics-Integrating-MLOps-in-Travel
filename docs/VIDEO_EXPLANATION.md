# Voyage Analytics — Video Explanation Script

A spoken walkthrough of the project, structured to the 8-section guideline
(~15 minutes total). Each section has a target duration, a speaker script,
and on-screen cues. Follow-up interview answers are at the end.

> **Stack alignment note (read once, then move on).** The project actually
> ships **FastAPI** (not Flask) and **GitHub Actions** (not Jenkins). The
> reasoning is identical — both are interchangeable in the same role —
> so the script uses the real stack. If you must say "Flask / Jenkins"
> for a course rubric, swap the words; the architecture is unchanged.

---

## 1. Introduction (1.5 min)

**On screen:** `README.md` + `docs/DOCUMENTATION.md` side by side, then the
project tree in the IDE.

> "Hi, I'm walking through **Voyage Analytics** — an end-to-end MLOps
> project in the **travel and tourism** domain. It's not a single model
> in a notebook; it's a deployable system that turns flight, hotel, and
> user data into three production ML services:
>
> 1. **Flight price prediction** — a regression model that estimates
>   ticket prices from route, airline, duration and distance.
> 2. **Gender classification** — a supervised classifier that predicts a
>   traveler's gender from profile fields like name, company and age.
> 3. **Hotel recommendations** — a content-based similarity model that
>   suggests similar hotels for a given booking.
>
> The stack is intentionally production-shaped: **Python 3.11** for the
> code, **FastAPI** for the REST layer, **Streamlit** for the user-facing
> dashboard, **MLflow** for experiment tracking, **DVC** for data
> versioning, **Apache Airflow** for scheduled retraining, **Docker** for
> packaging, **Kubernetes** for scalable serving, **Prometheus + Grafana**
> for monitoring, and **GitHub Actions** for CI/CD.
>
> The goal of this video is to show the **end-to-end system** — from raw
> CSV to a live API and dashboard — rather than just a trained model."

**Why this section matters:** the interviewer is checking that you can
articulate the *scope* of a production ML system in 90 seconds.

---

## 2. Problem Understanding (2 min)

**On screen:** `notebooks/eda/*.ipynb` quickly scrolling, then `src/api/app.py`.

> "Travel pricing and personalization are exactly the kind of problems
> ML is well suited to. Prices change with route, airline, season, and
> demand — there's no clean rule, but there *is* a strong statistical
> signal in historical bookings, so a regression model captures it
> better than any hand-coded heuristic. Recommendations are similar:
> users won't browse a full catalog, so we need a model that ranks the
> few most relevant hotels for them. And classification of profile data
> helps power **segmentation** and **personalization** downstream.
>
> But none of that matters if it lives only in a notebook.
> Productionization is where most ML projects fail:
>
> - A notebook can't serve a request from a mobile app.
> - A notebook can't be retrained on a schedule when data drifts.
> - A notebook can't be versioned, monitored, or rolled back.
>
> So this project treats ML as **four business tasks that need to run
> reliably**: prediction, classification, recommendation, and the
> automation around them. The four together — model + API + UI +
> orchestration — are what make it a system, not a script.
>
> The mental model I keep is: a notebook proves an idea works *once*;
> an MLOps pipeline guarantees it keeps working."

---

## 3. Data Understanding & Use-Case Mapping (2 min)

**On screen:** `data/raw/users.csv`, `data/raw/flights.csv`,
`data/raw/hotels.csv` opened in the IDE.

> "There are three datasets, and they map cleanly to the three use cases.
>
> - `**users.csv`** — traveler profiles: `code`, `name`, `gender`,
> `age`, `company`. This feeds the **gender classifier**.
> - `**flights.csv`** — bookings with `userCode`, `travelCode`,
> `from`, `to`, `flightType`, `agency`, `time`, `distance`,
> `price`, `date`. This feeds the **flight price regressor**.
> - `**hotels.csv`** — hotel bookings with `userCode`, `travelCode`,
> `name`, `place`, `days`, `price`, `total`, `date`. This feeds
> the **hotel recommender**.
>
> The three datasets connect through two foreign keys:
>
> - `**userCode`** links a flight or hotel booking back to the traveler
> in `users.csv` — so we can join demographic features onto bookings.
> - `**travelCode**` links a flight booking with the matching hotel
> booking from the same trip — so we can reason about full journeys.
>
> That join structure is what makes the platform a *travel* system
> rather than three unrelated models: the same `userCode` can flow
> through the gender classifier for personalization, the regressor for
> price expectations, and the recommender for hotel suggestions on the
> next trip."

---

## 4. Model Development & Serving Design (2.5 min)

**On screen:** `src/pipelines/training_pipeline.py`, then
`src/models/regression/train.py`, then `src/api/routes/prediction_routes.py`.

> "Three models, three sub-packages under `src/models/`:
> `regression/`, `classification/`, and `recommendation/`. They share
> the same upstream stages from `src/data/` and `src/features/`:
> ingestion → schema validation → date processing → feature engineering
> → preprocessing. That common backbone is what `TrainingPipeline` in
> `src/pipelines/training_pipeline.py` orchestrates.
>
> **Feature engineering** is mostly route-aware features for flights
> (origin–destination pairs, duration buckets, day-of-week from the
> booking date) and text-based features for hotels (TF-IDF on `name`
> and `place` for similarity). Preprocessing is wrapped in a
> `ColumnTransformer` so the *exact same* transformations applied at
> training are reused at inference — no train/serve skew.
>
> The regressor is exposed through **FastAPI**:
>
> - `POST /predict` — flight price
> - `POST /classify/gender` — traveler gender
>
> The request flow is straightforward:
>
> 1. Client sends JSON; Pydantic validates the schema.
> 2. The route handler calls a service in `src/api/services/`.
> 3. The service loads the trained pipeline from `artifacts/models/`,
>   transforms the input through the same preprocessor, runs `predict`,
>    and returns a JSON response with the prediction plus the inputs
>    echoed back for traceability.
> 4. If the artifact is missing, the API responds with a clear
>   `503 Service Unavailable` and the exact training command to run —
>    so the failure mode is operationally obvious.
>
> The crucial point: training and serving share the **same preprocessor
> object**, persisted to disk. That's what makes the model deployable."

---

## 5. MLOps Pipeline & Deployment (2 min)

**On screen:** `Dockerfile`, `kubernetes/deployment.yaml`,
`airflow/dags/training_dag.py`, `.github/workflows/mlops_ci.yaml`,
`mlruns/` folder.

> "Now the operational side — this is where the system earns the word
> 'MLOps'.
>
> - **Docker** packages the FastAPI service. The `Dockerfile` is built
> on `python:3.11-slim`, installs from a pinned `requirements.txt`,
> exposes port `8000`, and runs `uvicorn src.api.app:app`. One
> container, reproducible everywhere.
> - **Kubernetes** runs that image at scale. `kubernetes/deployment.yaml`
> defines the replicas, `service.yaml` exposes the API in-cluster, and
> `hpa.yaml` is a HorizontalPodAutoscaler that scales pods on CPU.
> That's how we go from one container to a fleet under traffic.
> - **GitHub Actions** is the CI/CD layer (the same role Jenkins plays in
> other stacks). `.github/workflows/mlops_ci.yaml` runs on every push
> to `main`: install deps, ensure datasets, run both training pipelines,
> verify the FastAPI app imports cleanly, and build the Docker image.
> That gates every change on a working, trainable, deployable system.
> - **Apache Airflow** owns *scheduled* work. The DAG
> `flight_price_training_pipeline` triggers `run_training_pipeline.py`
> daily — so the model is refreshed on new bookings without anyone
> running a script.
> - **MLflow** is the experiment and model store. Every training run
> logs parameters, metrics, and the trained pipeline artifact to
> `mlruns/` (backed by `mlflow.db`). That gives us run-to-run
> comparison, reproducibility, and a registry to promote a specific
> version into serving.
> - **DVC** versions the data and the pipeline itself. `dvc.yaml`
> declares the training stage with explicit deps and outs, so
> `dvc repro` re-runs only what's stale.
>
> Together: code in Git, data in DVC, experiments in MLflow, image in
> a registry, runtime in Kubernetes, schedule in Airflow. Nothing in
> the system is 'on someone's laptop'."

---

## 6. Recommendation Layer, App Interface & Monitoring (2 min)

**On screen:** `src/models/recommendation/similarity_engine.py`,
`streamlit_app/app.py` running in a browser, then
`docker-compose.monitoring.yml` and a Grafana dashboard.

> "The **recommender** is content-based. We build a TF-IDF representation
> over hotel `name` and `place`, compute cosine similarity, and for any
> query hotel return its top-K nearest neighbors. It's intentionally
> simple — no cold-start problem, no user-history dependency — and it's
> a strong baseline before moving to collaborative filtering.
>
> The **Streamlit dashboard** in `streamlit_app/` is the user-facing
> entry point. It has four pages:
>
> 1. **Flight Prediction** — form-based UI for the regressor.
> 2. **Hotel Recommendations** — pick a hotel, see top matches.
> 3. **Gender Classification** — try the classifier interactively.
> 4. **Analytics Dashboard** — Plotly charts of price distributions
>   and route trends.
>
> I chose Streamlit because it gets a Python ML team from `predict()`
> to a shareable web UI in a day, with no front-end build. The pages
> load models directly from `artifacts/models/`, so the dashboard works
> even when the API isn't running.
>
> **Monitoring** uses the FastAPI Prometheus instrumentator, which
> exposes `/metrics` on the API container. `docker-compose.monitoring.yml`
> spins up Prometheus + Grafana so we can watch request rate, latency,
> and error counts. There's also a `src/monitoring/drift_detector.py`
> hook for detecting input drift, which is the trigger for retraining."

---

## 7. Reliability, Challenges & Optimization (1.5 min)

**On screen:** `dvc.yaml`, `tests/` folder, `requirements.txt`.

> "The hard parts of this project weren't the models.
>
> **Challenges:**
>
> - *Three datasets, three schemas* — kept consistent through a single
> `src/data/schema.py` and an explicit `DataValidation` step that
> fails fast on bad columns or types.
> - *API design* — every endpoint validates with Pydantic, returns a
> clear `503` when the model artifact is missing, and tells the
> caller exactly which training script to run.
> - *Deployment complexity* — solved by treating the API as one
> container image and pushing all environment differences into
> Kubernetes manifests and configmaps.
> - *Workflow integration* — DVC, MLflow, Airflow, and CI all touch the
> same artifacts; the trick is making them agree on paths, which
> `configs/paths.yaml` centralizes.
>
> **Optimizations:**
>
> - Feature selection moved into the `ColumnTransformer` so it's
> serialized with the model and can't drift between train and serve.
> - The training pipeline is a single class with explicit stages, which
> is what made wrapping it as both a DVC stage and an Airflow task
> trivial.
> - The Docker image installs from a pinned `requirements.txt` for
> byte-for-byte reproducible builds.
>
> **Reliability comes from three things:** Git for code, DVC for data,
> MLflow for models. Every run is reproducible end-to-end."

---

## 8. Learnings & Future Improvements (1.5 min)

**On screen:** the project root, then a slide of "next steps".

> "The biggest lesson is the gap between **training a model** and
> **deploying a system**. Training is maybe 20% of the work — the other
> 80% is reproducibility, schemas, contracts, observability, and
> automation. Notebooks optimize for the 20%; this project optimizes
> for the other 80%.
>
> A few specific things I'd do next:
>
> - **Live model monitoring** — wire the drift detector into Prometheus
> alerts so a distribution shift triggers a retrain DAG automatically.
> - **Retraining pipelines** — promote the daily Airflow DAG into a
> *triggered* retraining flow that fires on drift or on new data
> landing, then registers the new MLflow version automatically.
> - **AuthN/AuthZ** — add OAuth2 / API-key auth to the FastAPI service
> before exposing it outside the cluster.
> - **Better recommendations** — move from TF-IDF to a hybrid model
> that combines content similarity with collaborative filtering on
> `userCode` + `travelCode` history.
> - **Cloud deployment** — push the image to ECR / GCR, manage secrets
> in a real KMS, and back MLflow with S3 + Postgres instead of the
> local SQLite store.
>
> The point is: the architecture is already shaped for these — none of
> them require rewriting the system, just extending it."

---

## Follow-up Interview Questions — Answer Cheat Sheet

### Q1. How would you productionize an ML model for real-time travel pricing?

> "Four pieces. **One**, freeze the preprocessing pipeline alongside the
> model — same `ColumnTransformer` at train and serve, persisted as a
> single artifact, so there's no train/serve skew. **Two**, expose it
> behind a typed REST contract — FastAPI + Pydantic gives you input
> validation, OpenAPI docs, and clear error codes for free. **Three**,
> make the deployment unit a container — Docker image built in CI,
> pushed to a registry, deployed via Kubernetes with an HPA so it scales
> on traffic. **Four**, instrument it — Prometheus metrics on the API,
> structured logging on every prediction, drift detection on inputs,
> and an MLflow model registry so you can roll back to a prior version
> in one command."

### Q2. Why did you use Docker and Kubernetes in this project?

> "Docker gives me a **reproducible runtime** — same Python version,
> same pinned dependencies, same code, regardless of who runs it.
> Kubernetes gives me **scale and resilience** — replicas, auto-scaling
> via HPA, rolling updates, self-healing pods, and a stable service
> endpoint. Together they let one image run identically on a laptop, in
> CI, and in production, and let the production fleet grow with traffic
> without code changes."

### Q3. How does MLflow help in managing model versions?

> "MLflow gives me three things. **Tracking** — every training run
> logs parameters, metrics, and the artifact, so I can compare runs
> objectively instead of arguing from memory. **Models** — runs are
> packaged as MLflow Models, which are loadable with a one-line
> `mlflow.sklearn.load_model(...)`. **Registry** — models get
> versioned and promoted through stages (Staging → Production), so the
> serving layer can pin to a stage rather than a file path. That makes
> rollbacks one config change away."

### Q4. How would you handle model retraining in production?

> "Two triggers, one pipeline. The **time trigger** is the daily Airflow
> DAG, which retrains on the latest data. The **event trigger** is the
> drift detector — when input distribution shifts beyond a threshold,
> it fires the same DAG immediately. The DAG runs the existing
> `TrainingPipeline`, logs the new run to MLflow, and only promotes the
> new version to Production if its validation metric beats the current
> Production model. The serving layer reads from the registry, so a
> promotion is picked up on the next pod restart — or via a rolling
> update with no downtime."

### Q5. How would you scale this system for a large travel platform?

> "Five layers. **Serving** — increase HPA limits, add a CDN/cache in
> front for repeated queries, and split per-model deployments so flight
> pricing scales independently of recommendations. **Data** — move raw
> data from CSV to a warehouse (BigQuery / Snowflake) and use Spark or
> dbt to build features at scale. **Feature store** — promote
> `data/feature_store/` into a real one (Feast) so training and serving
> share features with low-latency online lookup. **Training** — switch
> from local sklearn to distributed training (Ray, Dask, or
> SageMaker / Vertex AI) when the dataset outgrows one machine.
> **Operations** — back MLflow with a managed Postgres + S3, run
> Airflow on a managed service (MWAA / Cloud Composer), and put
> Prometheus + Grafana behind an alerting layer like PagerDuty. The
> code structure doesn't change — each component is replaced behind the
> same interface."

