import streamlit as st
import requests
import pandas as pd
import joblib
import plotly.express as px
import folium
from streamlit_folium import folium_static

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
    
# Streamlit UI
st.title("🌿 Real-Time Air Quality Index (AQI) Prediction")

# Sidebar for inputs
st.sidebar.title("Input Parameters")
api_key = st.sidebar.text_input("Enter your API Key:")
city_dict = {
    # india
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
    "Pune": (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Jaipur": (26.9124, 75.7873),
    "Lucknow": (26.8467, 80.9462),
    "Chandigarh": (30.7333, 76.7794),
    "Indore": (22.7196, 75.8577),
    "Bhopal": (23.2599, 77.4126),
    "Patna": (25.5941, 85.1376),
    "Bhubaneswar": (20.2961, 85.8245),
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Visakhapatnam": (17.6868, 83.2185),
    "Nagpur": (21.1458, 79.0882),
    "Coimbatore": (11.0168, 76.9558),
    "Vijayawada": (16.5062, 80.6480),
    "Guwahati": (26.1445, 91.7362),
    "Dehradun": (30.3165, 78.0322),
    "Ludhiana": (30.9010, 75.8573),
    "Agra": (27.1767, 78.0081),
    "Varanasi": (25.3176, 82.9739),
    "Mysore": (12.2958, 76.6394),
    "Ranchi": (23.3441, 85.3096),
    "Raipur": (21.2514, 81.6296),
    "Jodhpur": (26.2389, 73.0243),
    "Kochi": (9.9312, 76.2673),
    "Noida": (28.5355, 77.3910),
    "Ghaziabad": (28.6692, 77.4538),
    "Kanpur": (26.4499, 80.3319),
    "Surat": (21.1702, 72.8311),
    "Vadodara": (22.3072, 73.1812),
    "Gwalior": (26.2183, 78.1828),
    "Nashik": (19.9975, 73.7898),
    "Jabalpur": (23.1815, 79.9864), 
    # USA
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
    "San Francisco": (37.7749, -122.4194),

    # Europe
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Madrid": (40.4168, -3.7038),
    "Rome": (41.9028, 12.4964),

    # China
    "Beijing": (39.9042, 116.4074),
    "Shanghai": (31.2304, 121.4737),
    "Guangzhou": (23.1291, 113.2644),

    # Australia
    "Sydney": (-33.8688, 151.2093),
    "Melbourne": (-37.8136, 144.9631),

    # Middle East
    "Dubai": (25.276987, 55.296249),
    "Riyadh": (24.7136, 46.6753),
    "Tehran": (35.6892, 51.3890),

    # Africa
    "Cairo": (30.0444, 31.2357),
    "Lagos": (6.5244, 3.3792),
    "Johannesburg": (-26.2041, 28.0473),

    # South America
    "São Paulo": (-23.5505, -46.6333),
    "Buenos Aires": (-34.6037, -58.3816),
    "Lima": (-12.0464, -77.0428),

    # Canada
    "Toronto": (43.65107, -79.347015),
    "Vancouver": (49.2827, -123.1207)
}

city = st.sidebar.selectbox("Select a city:", list(city_dict.keys()))
latitude, longitude = city_dict[city]

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
        display_aqi_map(latitude, longitude, predicted_aqi)
        
        # Display AQI result
        st.subheader("🌡️ Predicted AQI")
        st.markdown(f"<h2 style='color:{color};'>{predicted_aqi:.2f} ({category})</h2>", unsafe_allow_html=True)
        st.warning(health_recommendations(predicted_aqi))

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
st.sidebar.write("Made with 💚 for Clean Air Awareness")
# Footer
st.markdown("---")
st.markdown("🌿 *Powered by AI | Developed with Streamlit*")
