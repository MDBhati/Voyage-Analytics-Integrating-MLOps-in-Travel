import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
os.chdir(_root)

import streamlit as st

from src.data.ingestion import DataIngestion
from src.models.recommendation.recommender import HotelRecommender


@st.cache_resource
def load_recommender():
    return HotelRecommender()


@st.cache_data
def load_hotel_names():
    return sorted(DataIngestion().load_hotels_data()["name"].dropna().unique())


recommender = load_recommender()
hotel_names = load_hotel_names()

st.title("Hotel Recommendation System")

hotel_name = st.selectbox("Select a hotel", options=hotel_names)

if st.button("Recommend Hotels"):
    try:
        recommendations = recommender.recommend(hotel_name)
    except (IndexError, KeyError):
        st.error(f"No hotel found matching '{hotel_name}'.")
    except FileNotFoundError:
        st.error(
            "Recommendation model not found at "
            "artifacts/models/hotel_recommender.pkl. "
            "Train it with: python run_recommendation_training.py"
        )
    except Exception as exc:
        st.error(f"Recommendation failed: {exc}")
    else:
        st.subheader("Recommended Hotels")
        for hotel in recommendations:
            st.write(hotel)
