import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
os.chdir(_root)

import pandas as pd
import streamlit as st

from src.data.ingestion import DataIngestion
from src.models.classification.predict import GenderClassifier


@st.cache_resource
def load_classifier():
    return GenderClassifier()


@st.cache_data
def load_users():
    return DataIngestion().load_users_data()


users_df = load_users()
classifier = load_classifier()

st.title("Gender Classification")
st.markdown(
    """
    Predict traveler **gender** (`male`, `female`, or `none`) from **name**,
    **company**, and **age** using the trained classifier in `artifacts/models/`.
    """
)

tab_predict, tab_explore = st.tabs(["Predict", "Dataset overview"])

with tab_predict:
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full name", value="Roy Braun")
        company = st.selectbox(
            "Company",
            options=sorted(users_df["company"].dropna().unique()),
        )

    with col2:
        age = st.number_input("Age", min_value=1, max_value=120, value=21)

    if st.button("Classify gender", type="primary"):
        input_df = pd.DataFrame(
            {"name": [name], "company": [company], "age": [age]}
        )

        try:
            predicted_gender, probabilities = classifier.predict(input_df)
            st.success(f"Predicted gender: **{predicted_gender}**")

            if probabilities:
                st.subheader("Class probabilities")
                prob_df = pd.DataFrame(
                    [{"gender": k, "probability": v} for k, v in probabilities.items()]
                ).sort_values("probability", ascending=False)
                st.bar_chart(prob_df.set_index("gender")["probability"])
        except FileNotFoundError:
            st.error(
                "Gender model not found. Train it with:\n\n"
                "`python run_gender_classification_training.py`"
            )
        except Exception as exc:
            st.error(f"Classification failed: {exc}")

with tab_explore:
    st.subheader("Users dataset")
    st.markdown(
        f"**{len(users_df):,}** traveler records · "
        f"**{users_df['gender'].nunique()}** gender labels"
    )

    gender_counts = users_df["gender"].value_counts().reset_index()
    gender_counts.columns = ["gender", "count"]
    st.bar_chart(gender_counts.set_index("gender")["count"])

    st.dataframe(users_df.head(20), use_container_width=True)
