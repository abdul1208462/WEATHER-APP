import requests
import streamlit as st
import time
import re

st.set_page_config(page_title="Weather App", page_icon="🌦")

API_KEY = st.secrets["API_KEY"]

st.title("🌦 Weather Forecast App")
if "last_request" not in st.session_state:
    st.session_state.last_request = 0

city = st.text_input("Enter City Name")
event = st.selectbox(
    "Select Your Event",
    [
        "None",
        "Wedding",
        "Cricket Match",
        "Picnic",
        "Construction Work",
        "Bike Ride"
    ]
)


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
    return "🌍"

def weather_advice(temp, weather_id, wind, event):
    rain = 200 <= weather_id <= 531
    snow = 600 <= weather_id <= 622

    if rain:
        outside = "❌ No. Rain is expected."
    elif snow:
        outside = "❌ No. Snow is expected."
    elif wind > 12:
        outside = "⚠ Strong winds. Go only if necessary."
    elif temp >= 38:
        outside = "⚠ Extremely hot outside."
    elif temp <= 5:
        outside = "⚠ Very cold outside."
    else:
        outside = "✅ Yes! Weather looks good."

    event_msg = ""

    if event == "Wedding":
        event_msg = "💍 Suitable for an outdoor wedding." if not rain else "💍 Better move the wedding indoors."

    elif event == "Cricket Match":
        event_msg = "🏏 Great weather for cricket." if not rain and wind < 10 else "🏏 Match may be affected."

    elif event == "Picnic":
        event_msg = "🧺 Perfect day for a picnic." if not rain and temp < 35 else "🧺 Picnic is not recommended."

    elif event == "Construction Work":
        event_msg = "🏗 Construction can continue safely." if not rain else "🏗 Rain may delay construction."

    elif event == "Bike Ride":
        event_msg = "🏍 Enjoy your ride." if not rain and wind < 10 else "🏍 Riding is not recommended."

    return outside, event_msg


if st.button("Get Weather"):

    # Remove extra spaces
    city = city.strip()

    # Check if input is empty
    if not city:
        st.error("Please enter a city name.")
        st.stop()

    # Maximum length
    if len(city) > 50:
        st.error("City name is too long.")
        st.stop()

    # Allow only letters, spaces, hyphens and apostrophes
    if not re.fullmatch(r"[A-Za-z\s\-']+", city):
        st.error("Invalid city name. Only letters, spaces, hyphens (-), and apostrophes (') are allowed.")
        st.stop()

    # Rate limiting
    current_time = time.time()

    if current_time - st.session_state.last_request < 10:
        st.warning("⏳ Please wait 10 seconds before making another request.")
        st.stop()

    st.session_state.last_request = current_time

    current_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:

        current = requests.get(current_url).json()

        if str(current["cod"]) != "200":
            st.error(current)
            st.stop()
       

        temp = current["main"]["temp"]
        humidity = current["main"]["humidity"]
        wind = current["wind"]["speed"]
        country = current["sys"]["country"]

        weather_id = current["weather"][0]["id"]
        description = current["weather"][0]["description"]

        icon = current["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

        st.image(icon_url, width=120)

        st.markdown(f"# {get_weather_emoji(weather_id)}")
        st.metric("Temperature", f"{temp:.1f} °C")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Humidity", f"{humidity}%")

        with col2:
            st.metric("Wind Speed", f"{wind} m/s")

        with col3:
            st.metric("Country", country)

        st.subheader(description.title())

        st.divider()

        st.subheader("🤔 Should I Go Outside Today?")

        outside, event_result = weather_advice(
            temp,
            weather_id,
            wind,
            event
        )

        st.success(outside)

        if event != "None":
            st.info(event_result)
        


        st.divider()

        st.subheader("5-Day Forecast")

        forecast = requests.get(forecast_url).json()

        shown_days = set()

        for item in forecast["list"]:
            date = item["dt_txt"].split()[0]

            if date not in shown_days:
                shown_days.add(date)

                temp = item["main"]["temp"]
                desc = item["weather"][0]["description"]

                st.write(
                    f"📅 {date} | 🌡 {temp:.1f}°C | {desc.title()}"
                )

                if len(shown_days) >= 5:
                    break

    except Exception as e:
        st.error(str(e))

