import streamlit as st

st.set_page_config(
    page_title="Voyage Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Voyage Analytics Platform")
st.caption(
    "Travel data analytics, flight price prediction, and hotel recommendations "
    "— powered by trained ML artifacts and an MLOps-ready stack."
)

st.markdown(
    """
    **Voyage Analytics** turns flight and hotel booking data into insights and
    interactive ML services. Use the sidebar to explore each capability, or
    read below for how this dashboard fits into the project.
    """
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Flight price prediction")
    st.markdown(
        """
        Estimate ticket prices from **origin**, **destination**, **flight class**,
        **agency**, **duration**, and **distance**.

        Models are loaded from `artifacts/models/` — no API required for the UI.
        """
    )
    st.page_link(
        "pages/flight_prediction.py",
        label="Open Flight Prediction →",
        icon="🛫",
    )

with col2:
    st.subheader("Hotel recommendations")
    st.markdown(
        """
        Get **similar hotels** using content-based similarity on location and name.
        Pick a hotel from the dataset and view the top matches instantly.
        """
    )
    st.page_link(
        "pages/hotel_recommendation.py",
        label="Open Hotel Recommendations →",
        icon="🏨",
    )

with col3:
    st.subheader("Gender classification")
    st.markdown(
        """
        Classify traveler **gender** from name, company, and age using a
        supervised model trained on the users dataset.
        """
    )
    st.page_link(
        "pages/gender_classification.py",
        label="Open Gender Classification →",
        icon="👤",
    )

with col4:
    st.subheader("Travel analytics")
    st.markdown(
        """
        Explore **price distributions** and **route-level trends** across the
        flights dataset with interactive Plotly charts.
        """
    )
    st.page_link(
        "pages/analytics_dashboard.py",
        label="Open Analytics Dashboard →",
        icon="📊",
    )

st.divider()

st.subheader("Project objectives")

obj_left, obj_right = st.columns(2)

with obj_left:
    st.markdown(
        """
        - **Predict** flight prices with regression models trained on historical routes
        - **Classify** traveler gender from profile features (name, company, age)
        - **Recommend** hotels using TF-IDF similarity on place and name features
        - **Analyze** booking patterns to support pricing and operations decisions
        """
    )

with obj_right:
    st.markdown(
        """
        - **Track** experiments with MLflow and version data with DVC
        - **Automate** training with Airflow DAGs and deploy via Docker / Kubernetes
        - **Monitor** serving with Prometheus metrics, logging, and drift detection
        """
    )

with st.expander("Datasets used in this project"):
    st.markdown(
        """
        | Dataset | Description |
        |---------|-------------|
        | **Flights** | Routes, agencies, duration, distance, price, dates |
        | **Hotels** | Bookings, places, hotel names, stay length, pricing |
        | **Users** | Traveler profiles for classification workflows |
        """
    )

with st.expander("REST API (optional)"):
    st.markdown(
        """
        The FastAPI service exposes the same flight prediction logic for programmatic use.

        - **Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
        - **Health:** `GET /health`
        - **Predict:** `POST /predict`
        - **Classify gender:** `POST /classify/gender`

        Start the API from the project root:

        ```bash
        uvicorn src.api.app:app --reload --port 8000
        ```
        """
    )

st.info(
    "Tip: Select a page in the sidebar to get started. "
    "All ML pages load models from `artifacts/models/` on first use."
)
