from src.data.ingestion import DataIngestion

ingestion = DataIngestion()

flights_df = ingestion.load_flights_data()
hotels_df = ingestion.load_hotels_data()
users_df = ingestion.load_users_data()

print(flights_df.head())
print(hotels_df.head())
print(users_df.head())