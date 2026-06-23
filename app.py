
import requests
import streamlit as st

st.set_page_config(page_title="Weather App", page_icon="🌦")

API_KEY = st.secrets["85c9c74e55a160c908f4825d97ea5dfd"]

st.title("🌦 Weather Forecast App")

city = st.text_input("Enter City Name")


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


if st.button("Get Weather"):

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

        if current["cod"] != 200:
            st.error("City not found")
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

