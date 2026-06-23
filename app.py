import requests
import streamlit as st

API_KEY = "831f0dda186c1c1e586b492a727b9a9c"

st.set_page_config(page_title="Weather App")

st.title("🌦 Weather App")

city = st.text_input("Enter city name")

def get_weather_emoji(weather_id):
    if 200 <= weather_id <= 232:
        return "⛈"
    elif 300 <= weather_id <= 321:
        return "🌦"
    elif 500 <= weather_id <= 531:
        return "🌧"
    elif 600 <= weather_id <= 622:
        return "❄"
    elif 701 <= weather_id <= 741:
        return "🌫"
    elif weather_id == 762:
        return "🌋"
    elif weather_id == 771:
        return "💨"
    elif weather_id == 781:
        return "🌪"
    elif weather_id == 800:
        return "☀"
    elif 801 <= weather_id <= 804:
        return "☁"
    return ""

if st.button("Get Weather"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15

        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"]

        st.metric("Temperature", f"{temperature_c:.1f} °C")
        st.markdown(f"# {get_weather_emoji(weather_id)}")
        st.write(description.title())

    except requests.exceptions.HTTPError:
        st.error("City not found or API error")
    except requests.exceptions.ConnectionError:
        st.error("Check your internet connection")
    except requests.exceptions.Timeout:
        st.error("Request timed out")
    except Exception as e:
        st.error(str(e))