import streamlit as st
import requests
import pandas as pd
import joblib
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Load model and scaler
model = joblib.load('aqi_model.pkl')
scaler = joblib.load('scaler.pkl')

# Function to predict AQI
def predict_aqi(real_time_data):
    real_time_df = pd.DataFrame([real_time_data])
    real_time_scaled = scaler.transform(real_time_df)
    prediction = model.predict(real_time_scaled)
    return prediction[0]

# Fetch real-time air quality data
def fetch_real_time_data(api_key, lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    pollutants = data['list'][0]['components']
    real_time_data = {
        'PM2.5': pollutants['pm2_5'],
        'PM10': pollutants['pm10'],
        'NO': pollutants.get('no', 0),
        'NO2': pollutants['no2'],
        'NOx': pollutants.get('nox', 0),
        'NH3': pollutants['nh3'],
        'CO': pollutants['co'],
        'SO2': pollutants['so2'],
        'O3': pollutants['o3'],
        'Benzene': 0,
        'Toluene': 0,
        'Xylene': 0
    }
    return real_time_data

# Function to classify AQI
def classify_aqi(aqi):
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Moderate", "yellow"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "orange"
    elif aqi <= 200:
        return "Unhealthy", "red"
    elif aqi <= 300:
        return "Very Unhealthy", "purple"
    else:
        return "Hazardous", "maroon"

# Function to display AQI map
def display_aqi_map(lat, lon, aqi):
    m = folium.Map(location=[lat, lon], zoom_start=10)
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        popup=f"AQI: {aqi}",
        color="red" if aqi > 150 else "orange" if aqi > 100 else "green",
        fill=True
    ).add_to(m)
    folium_static(m)

# Function to provide health recommendations
def health_recommendations(aqi):
    if aqi <= 50:
        return "Air quality is good. Enjoy outdoor activities!"
    elif aqi <= 100:
        return "Moderate air quality. Sensitive individuals should reduce prolonged outdoor exertion."
    elif aqi <= 150:
        return "Unhealthy for sensitive groups. Consider limiting outdoor exposure."
    elif aqi <= 200:
        return "Unhealthy air. Everyone should reduce outdoor activities."
    elif aqi <= 300:
        return "Very unhealthy. Stay indoors and wear a mask if going out."
    else:
        return "Hazardous air. Avoid going outside and use air purifiers indoors."

# Function to plot AQI trends
def plot_aqi_trends(data):
    df = pd.DataFrame([data])
    fig = px.bar(
        df.melt(var_name="Pollutant", value_name="Concentration"),
        x="Pollutant",
        y="Concentration",
        title="Air Pollutant Levels",
        color="Pollutant"
    )
    st.plotly_chart(fig)

# Streamlit Sidebar UI
st.sidebar.title("Real-Time AQI Prediction")
api_key = st.sidebar.text_input("Enter your API Key:")

city_dict = {
    "Delhi": (28.6139, 77.2090),
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Beijing": (39.9042, 116.4074)
}

city = st.sidebar.selectbox("Select a city:", list(city_dict.keys()))
latitude, longitude = city_dict[city]

if st.sidebar.button("Get Real-Time AQI Prediction"):
    if api_key:
        real_time_data = fetch_real_time_data(api_key, latitude, longitude)
        predicted_aqi = predict_aqi(real_time_data)
        aqi_category, color = classify_aqi(predicted_aqi)

        st.sidebar.write("### Real-time Air Quality Data:", real_time_data)
        st.sidebar.success(f"Predicted AQI: {predicted_aqi:.2f}")
        st.sidebar.markdown(f"### AQI Category: <span style='color:{color}'>{aqi_category}</span>", unsafe_allow_html=True)
        st.sidebar.warning(health_recommendations(predicted_aqi))
        plot_aqi_trends(real_time_data)
        display_aqi_map(latitude, longitude, predicted_aqi)
    else:
        st.sidebar.error("Please enter a valid API key.")
