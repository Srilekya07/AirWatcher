import streamlit as st
import requests
import pandas as pd
import joblib
import plotly.express as px

# Load the trained model and scaler
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

# AQI Category Interpretation
def get_aqi_category(aqi):
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

# Streamlit UI
st.title("🌿 Real-Time Air Quality Index (AQI) Prediction")

# Sidebar for inputs
st.sidebar.title("Input Parameters")
api_key = st.sidebar.text_input("Enter your API Key:")
latitude = st.sidebar.number_input("Enter Latitude:", value=28.6139)
longitude = st.sidebar.number_input("Enter Longitude:", value=77.2090)

# Main button
if st.sidebar.button("Get Real-Time AQI Prediction"):
    if api_key:
        with st.spinner("Fetching real-time data..."):
            real_time_data = fetch_real_time_data(api_key, latitude, longitude)
            predicted_aqi = predict_aqi(real_time_data)
            category, color = get_aqi_category(predicted_aqi)

        # Display pollutant levels as a bar chart
        st.subheader("📊 Real-time Air Quality Data")
        pollutants_df = pd.DataFrame(real_time_data.items(), columns=['Pollutant', 'Concentration (µg/m³)'])
        fig = px.bar(pollutants_df, x='Pollutant', y='Concentration (µg/m³)', color='Pollutant', title='Pollutant Concentrations')
        st.plotly_chart(fig)

        # Display AQI result
        st.subheader("🌡️ Predicted AQI")
        st.markdown(f"<h2 style='color:{color};'>{predicted_aqi:.2f} ({category})</h2>", unsafe_allow_html=True)

    else:
        st.sidebar.error("Please enter a valid API key.")

# Option to upload historical data
st.sidebar.markdown("---")
st.sidebar.title("📁 Upload Historical Data for Analysis")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.subheader("📈 Historical Data Preview")
    st.dataframe(data.head())

    if 'AQI' in data.columns:
        fig = px.line(data, x=data.index, y='AQI', title='Historical AQI Trends')
        st.plotly_chart(fig)
    else:
        st.sidebar.warning("CSV file must contain an 'AQI' column.")

# Footer
st.markdown("---")
st.markdown("🌿 *Powered by AI | Developed with Streamlit*")
