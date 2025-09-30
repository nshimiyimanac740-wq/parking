# parking_app.py
import streamlit as st
import pandas as pd
import pickle

# -----------------------------
# Load the saved model and encoders
# -----------------------------
with open("parking_model.pkl", "rb") as f:
    parking_model = pickle.load(f)

with open("le_day.pkl", "rb") as f:
    le_day = pickle.load(f)

with open("le_weather.pkl", "rb") as f:
    le_weather = pickle.load(f)

# -----------------------------
# Streamlit App UI
# -----------------------------
st.title("Parking Space Prediction App 🚗")

# User input
day_input = st.selectbox("Day", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
hour_input = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
weather_input = st.selectbox("Weather", ["Sunny","Rainy","Cloudy"])
weekend_input = st.selectbox("Weekend", ["Yes", "No"])
event_input = st.selectbox("Nearby Event", ["Yes", "No"])
occupied_last_hour_input = st.selectbox("Occupied Last Hour", ["Yes", "No"])

# Encode categorical inputs
day_encoded = le_day.transform([day_input])[0]
weather_encoded = le_weather.transform([weather_input])[0]
weekend_encoded = 1 if weekend_input == "Yes" else 0
event_encoded = 1 if event_input == "Yes" else 0
occupied_last_hour_encoded = 1 if occupied_last_hour_input == "Yes" else 0

# Create dataframe for prediction
input_df = pd.DataFrame({
    "Day": [day_encoded],
    "Hour": [hour_input],
    "Weather": [weather_encoded],
    "Weekend": [weekend_encoded],
    "NearbyEvent": [event_encoded],
    "OccupiedLastHour": [occupied_last_hour_encoded]
})

# Prediction
prediction = parking_model.predict(input_df)[0]

# Display result
if prediction == 1:
    st.success("✅ There is an empty parking space. You can ENTER INSIDE.")
else:
    st.error("❌ No PARKING AVAILABLE. STOP PLEASE")

