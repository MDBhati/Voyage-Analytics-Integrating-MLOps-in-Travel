# Voyage Analytics — Slide Outline

A one-page slide deck to show alongside the video narration. **10 slides**,
mapped 1:1 to the sections of `docs/VIDEO_EXPLANATION.md`. Keep each slide
visually light — the script does the talking.

---

### Slide 1 — Title

> **Voyage Analytics**
> *An end-to-end MLOps platform for travel & tourism*

- Your name · date
- Tagline: *"From CSV to live API — three ML services, one production system."*
- Background image: airplane silhouette / world map (subtle)

---

### Slide 2 — What I Built (Section 1, 1.5 min)

**Three production ML services on one stack**

| Capability | Type | Endpoint / UI |
|---|---|---|
| Flight price prediction | Regression | `POST /predict` |
| Gender classification | Classification | `POST /classify/gender` |
| Hotel recommendations | Content-based | Streamlit page |

**Stack icons row:** Python · FastAPI · Streamlit · MLflow · DVC · Airflow · Docker · Kubernetes · Prometheus · GitHub Actions

---

### Slide 3 — Why ML, Why Production (Section 2, 2 min)

**Notebook ≠ System**

- Notebook proves an idea works **once**
- Pipeline guarantees it keeps working — at scale, on schedule, with rollback

**Four business tasks**
- Predict · Classify · Recommend · Automate

**Visual:** split image — *Notebook* (one machine, one user) vs *Production* (cluster, many users, monitoring).

---

### Slide 4 — Data Map (Section 3, 2 min)

**Three datasets, two foreign keys, three use cases**

```
users.csv ──userCode──┐
                       ├──► gender classifier
                       │
flights.csv ──userCode─┘
            └─travelCode─┐
                          ├──► price regressor
hotels.csv ──userCode─────┘
            └─travelCode─────► hotel recommender
```

- `userCode` → joins demographics onto bookings
- `travelCode` → links flights ↔ hotels for the same trip

---

### Slide 5 — Model & Serving Design (Section 4, 2.5 min)

**Same backbone, three model heads**

```
ingest → validate → preprocess → feature engineer
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                          ▼
        Regression               Classification              Recommendation
        (flight price)            (gender)                   (TF-IDF + cosine)
            │                          │                          │
            └────────────► artifacts/models/ ◄────────────────────┘
                                       │
                                FastAPI + Streamlit
```

**Key idea:** `ColumnTransformer` is persisted *with* the model → no train/serve skew.

---

### Slide 6 — MLOps Pipeline (Section 5, 2 min)

**Where each tool lives**

| Tool | Role |
|---|---|
| **Docker** | Reproducible runtime image |
| **Kubernetes** | Replicas + HPA scaling |
| **GitHub Actions** | CI/CD on every push |
| **Apache Airflow** | Daily retraining DAG |
| **MLflow** | Experiment tracking + model registry |
| **DVC** | Data + pipeline versioning |

**One-liner:** *Code in Git · Data in DVC · Experiments in MLflow · Image in Registry · Runtime in K8s · Schedule in Airflow*

---

### Slide 7 — Recommender, App & Monitoring (Section 6, 2 min)

**Recommendation:** TF-IDF on `name` + `place` → cosine similarity → top-K

**Streamlit dashboard — 4 pages**
- Flight Prediction · Hotel Recommendations · Gender Classification · Analytics

**Monitoring**
- `/metrics` (Prometheus instrumentator on FastAPI)
- Grafana dashboards (`docker-compose.monitoring.yml`)
- Drift detector → retraining trigger

---

### Slide 8 — Reliability & Optimization (Section 7, 1.5 min)

**Challenges**
- 3 schemas → centralized in `src/data/schema.py`
- Missing artifacts → clear `503` with training command
- Path drift across tools → unified in `configs/paths.yaml`

**Optimizations**
- Feature selection inside `ColumnTransformer`
- Pinned `requirements.txt` for byte-reproducible builds
- Single training class → reused as DVC stage *and* Airflow task

**Reliability rests on three things:** Git · DVC · MLflow

---

### Slide 9 — Learnings & Roadmap (Section 8, 1.5 min)

**Lesson:** Training is 20% — reproducibility, schemas, observability are the other 80%.

**Next**
- Drift-triggered auto-retraining
- AuthN/AuthZ on the API
- Hybrid recommender (content + collaborative)
- Cloud-managed MLflow (S3 + Postgres) and Airflow (MWAA / Composer)

---

### Slide 10 — Q&A Anchors

Quick reference cards for the five follow-up questions:

| # | Question | One-line answer |
|---|---|---|
| 1 | Productionize real-time pricing? | Frozen pipeline + typed API + container + monitoring + registry |
| 2 | Why Docker + K8s? | Reproducibility + scale & self-healing |
| 3 | What does MLflow give you? | Tracking · Models · Registry → 1-command rollback |
| 4 | How would you retrain? | Time trigger (Airflow daily) + event trigger (drift) → same DAG → MLflow promotion |
| 5 | How would you scale? | 5 layers: serving · data · feature store · training · ops |

---

### Presentation tips

- **Pace:** ~1 slide per 1.5 min on average — slides 5 and 6 deserve more time, slide 1 less.
- **Show, don't read:** when on slide 5 or 6, alt-tab into the IDE briefly to point at the actual file.
- **Demo (optional, +2 min):** end with a live `curl` to `/predict` and the Streamlit prediction page.
