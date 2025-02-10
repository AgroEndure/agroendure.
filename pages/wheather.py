import streamlit as st
import requests

# Set Streamlit Page Configuration
st.set_page_config(page_title="Weather App", page_icon="🌦️", layout="centered")

# Main function to run the Streamlit app
def main():
    # Title with emoji
    st.title("🌦️ Weather Forecasting with LLM")
    st.write("Get real-time weather updates and a 3-day forecast for any city!")

    # Sidebar configuration
    st.sidebar.header("🔍 Search City")
    city = st.sidebar.text_input("Enter city name", "London")

    # API key (Replace with your OpenWeatherMap API key)
    weather_api_key = "bdcd8d585dc181460feba0a23460b09e"

    # Button to fetch and display weather data
    if st.sidebar.button("🔎 Get Weather"):
        # Fetch current weather
        current_weather = get_current_weather(city, weather_api_key)
        # Fetch forecast weather
        forecast_weather = get_weather_forecast(city, weather_api_key)

        if current_weather:
            # Display Current Weather
            st.markdown("## ☀️ Current Weather")
            st.write(f"📍 **Location:** {city}")

            # Use columns for better layout
            col1, col2, col3 = st.columns(3)
            col1.metric("🌡 Temperature", f"{current_weather['main']['temp']}°C")
            col2.metric("💧 Humidity", f"{current_weather['main']['humidity']}%")
            col3.metric("🌬 Wind Speed", f"{current_weather['wind']['speed']} m/s")

            st.divider()

        else:
            st.error("❌ Could not fetch current weather. Check API key or city name.")

        if forecast_weather:
            # Display Weather Forecast
            st.markdown("##  3-Day Weather Forecast")
            for day in forecast_weather:
                with st.container():
                    st.markdown(f"### 📅 {day['date']}")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("🌡 Temperature", f"{day['temp']}°C")
                    col2.metric("🌧 Rain Probability", f"{day['rain']}%")
                    col3.metric("💧 Humidity", f"{day['humidity']}%")
                    st.markdown("---")
        else:
            st.error("❌ Could not fetch weather forecast. Check API key or city name.")

# Function to fetch current weather
def get_current_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to fetch 3-day weather forecast
def get_weather_forecast(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        forecast_data = []
        
        # Extract 3-day forecast at 12:00 PM daily
        dates_processed = set()
        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]
            if date not in dates_processed and "12:00:00" in entry["dt_txt"]:
                forecast_data.append({
                    "date": date,
                    "temp": entry["main"]["temp"],
                    "rain": entry.get("rain", {}).get("3h", 0),  # Rain in last 3 hours (0 if missing)
                    "humidity": entry["main"]["humidity"]
                })
                dates_processed.add(date)
            if len(forecast_data) == 3:  # Limit to 3 days
                break
        
        return forecast_data
    return None

if __name__ == "__main__":
    main()
