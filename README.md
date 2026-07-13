# 🌦 Weather Forecast App

A simple Weather Forecast web application built using **Python**, **Streamlit**, and the **OpenWeatherMap API**.

## Features

- 🌡 Current temperature (°C)
- 💧 Humidity
- 🌬 Wind speed
- 🌍 Country name
- 🌤 Weather description
- 🌦 Weather emoji
- 🖼 Weather icon
- 📅 5-day weather forecast
- 🔒 Secure API key using Streamlit Secrets

## Technologies Used

- Python
- Streamlit
- Requests
- OpenWeatherMap API

## Project Structure

```
Weather-App/
│── app.py
│── requirements.txt
│── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/abdul1208462/WEATHER-APP.git
cd WEATHER-APP
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get an API Key

Create a free account at:

https://openweathermap.org/api

Generate an API key.

### 4. Create Streamlit Secrets

Create the file:

```
.streamlit/secrets.toml
```

Add:

```toml
API_KEY = "YOUR_API_KEY"
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

## Live Demo
https://weather-app-nvsvhaviqlu5zaybw3aosh.streamlit.app/

## How It Works

1. Enter a city name.
2. Click **Get Weather**.
3. The app sends a request to the OpenWeatherMap API.
4. The API returns weather information in JSON format.
5. The application displays:
   - Temperature
   - Weather condition
   - Humidity
   - Wind speed
   - Country
   - Weather icon
   - 5-day forecast
