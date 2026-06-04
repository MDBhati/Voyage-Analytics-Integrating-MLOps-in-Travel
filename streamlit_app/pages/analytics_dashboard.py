import streamlit as st
import plotly.express as px

from src.data.ingestion import DataIngestion

ingestion = DataIngestion()

flights_df = (
    ingestion.load_flights_data()
)

st.title(
    "Travel Analytics Dashboard"
)

fig = px.histogram(

    flights_df,

    x="price",

    title="Flight Price Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

route_fig = px.bar(

    flights_df.groupby(
        "from"
    )["price"].mean().reset_index(),

    x="from",

    y="price",

    title="Average Price by Origin"
)
st.plotly_chart(
    route_fig,
    use_container_width=True
)
