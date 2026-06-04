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
from src.models.regression.predict import FlightPricePredictor


@st.cache_resource
def load_predictor():
    return FlightPricePredictor()


@st.cache_data
def load_flights():
    return DataIngestion().load_flights_data()


flights_df = load_flights()
predictor = load_predictor()

st.title("Flight Price Prediction")

from_locations = sorted(flights_df["from"].dropna().unique())
to_locations = sorted(flights_df["to"].dropna().unique())
flight_types = sorted(flights_df["flightType"].dropna().unique())
agencies = sorted(flights_df["agency"].dropna().unique())

from_location = st.selectbox("From", options=from_locations)
to_location = st.selectbox("To", options=to_locations)
flight_type = st.selectbox("Flight Type", options=flight_types)
agency = st.selectbox("Agency", options=agencies)

time = st.number_input("Flight Duration (hours)", min_value=0.0, value=1.0, step=0.01)
distance = st.number_input("Distance (km)", min_value=0.0, value=100.0, step=1.0)

if st.button("Predict Price"):
    input_df = pd.DataFrame(
        {
            "from": [from_location],
            "to": [to_location],
            "flightType": [flight_type],
            "agency": [agency],
            "time": [time],
            "distance": [distance],
        }
    )

    try:
        predicted_price = predictor.predict(input_df)
        st.success(f"Predicted Price: ${float(predicted_price):,.2f}")
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
