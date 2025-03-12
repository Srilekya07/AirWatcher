# 🌿 AirWatcher, A Real-Time Air Quality Prediction System
## 📋 Project Overview
"This project develops an AI-powered model using machine learning techniques to predict Air Quality Index (AQI) based on environmental data fetched from the OpenWeatherMap API and visualizes pollutant levels and AQI categories interactively. It aims to provide accurate forecasts, helping in proactive pollution management and public health awareness."

## ✨ Features

- Real-time AQI Prediction: Uses pollutant data (PM2.5, PM10, NO2, CO, etc.) to predict AQI.

- Interactive UI: Built with Streamlit for a user-friendly interface.

- Data Visualization: Displays pollutant concentrations using dynamic bar charts.

- AQI Interpretation: Shows AQI categories (Good, Moderate, Unhealthy, etc.) with color-coded results.

- Historical Data Analysis: Allows users to upload CSV files for custom data analysis.

- Real-time Data Fetch: Integrates with OpenWeatherMap's Air Pollution API.

## 🚀 Tech Stack

**Programming Language:** Python

**Libraries:** Streamlit, Pandas, NumPy, Scikit-learn, Joblib, Requests, Plotly

**Machine Learning Model:** Random Forest Regressor (or Linear Regression, based on your choice)

**API:** OpenWeatherMap Air Pollution API

## 📦 Project Structure
```
├── aqi_app.py                  # Main Streamlit app for real-time AQI prediction
├── aqi_model.pkl               # Trained ML model
├── scaler.pkl                  # Scaler for input feature normalization
├── air_quality_data.csv         # Sample dataset for training/testing
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies
```
## 📊 How to Run the Project

**1. Clone the repository** 
```
git clone https://github.com/yourusername/aqi-prediction.git
cd aqi-prediction
 ```
**2. Install dependencies**
 ```
pip install -r requirements.txt
 ```
**3. Run the Streamlit app**
 ```
streamlit run aqi_app.py
 ```
**4. Interact with the app**
- Enter your OpenWeatherMap API key.

- Input latitude and longitude to fetch real-time air quality data.

- Click Get Real-Time AQI Prediction.

- View the pollutant chart and AQI result.

- Optionally, upload a CSV file to analyze historical AQI data.

## 🌐 How to Get OpenWeatherMap API Key
1. Sign up at OpenWeatherMap.

2. Go to API Keys under your profile.

3. Copy the API key and paste it into the app when prompted.

 ## 💡 Future Improvements
- Live AQI Map: Display AQI levels on an interactive map.

- Push Notifications: Alert users for hazardous AQI levels.

- Multiple Models: Allow users to choose different ML models for prediction.

- Cloud Deployment: Host the app on platforms like Heroku or AWS.
  
 ## 📧 Contact

For any questions or feedback, feel free to reach out!
