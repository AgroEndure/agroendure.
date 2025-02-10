import streamlit as st
import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
from dotenv import load_dotenv
import os
import openai
from pathlib import Path

# Load environment variables from a .env file
load_dotenv()

# Configure API keys
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load dummydata.csv file into pandas DataFrame
def load_data_from_csv(file_path="dummydata.csv"):
    data = pd.read_csv(file_path, header=None)
    nitrogen, phosphorus, potassium, ph_value, moisture = data.iloc[0].values
    return nitrogen, phosphorus, potassium, ph_value, moisture

# Streamlit UI
st.title("AgroEndure: Plant Health and Crop Management")

# Crop Recommendation and Weather Section
st.header("Crop Recommendation based on Soil NPK and Weather")

# Function to update the values from the CSV file when the button is clicked
def update_values_from_csv():
    nitrogen, phosphorus, potassium, ph_value, moisture = load_data_from_csv()
    st.session_state.n_value = nitrogen
    st.session_state.p_value = phosphorus
    st.session_state.k_value = potassium
    st.session_state.ph_value = ph_value
    st.session_state.moisture = moisture

# Add a button to reload the latest values from the CSV file
if st.button("Load Latest Data from CSV"):
    update_values_from_csv()
    st.success("Latest values loaded from CSV!")

# Display current values from session state or initial default values
n_value = st.number_input("Nitrogen (N)", value=st.session_state.get("n_value", 5.2))
p_value = st.number_input("Phosphorus (P)", value=st.session_state.get("p_value", 3.1))
k_value = st.number_input("Potassium (K)", value=st.session_state.get("k_value", 6.7))
ph_value = st.number_input("pH Value", value=st.session_state.get("ph_value", 6.5))

# Target year and date range input fields
target_year = st.text_input("Target Year", "2023")
start_month = st.text_input("Start Month", "1")
start_day = st.text_input("Start Day", "1")
end_month = st.text_input("End Month", "12")
end_day = st.text_input("End Day", "31")

# Function to query GPT-3.5-turbo with NPK values and get plant recommendations
def get_plant_recommendation(n, p, k):
    prompt = f"""
    Based on the following soil NPK values:
    Nitrogen (N): {n}
    Phosphorus (P): {p}
    Potassium (K): {k}
    Recommend the best crops or plants that would grow optimally in this soil. Provide a brief explanation for each crop recommendation, considering its nutrient requirements.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an expert in soil science and agriculture."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
            n=1
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function to fetch weather data for a specific year range
def get_weather_data(target_year, start_month, start_day, end_month, end_day):
    lahore = Point(31.5497, 74.3436, 217)
    years_to_analyze = 3
    combined_data = pd.DataFrame()

    target_year = int(target_year)
    start_month = int(start_month)
    start_day = int(start_day)
    end_month = int(end_month)
    end_day = int(end_day)

    for year in range(target_year - 1, target_year - years_to_analyze - 1, -1):
        start = datetime(year, start_month, start_day)
        end = datetime(year, end_month, end_day)
        data = Daily(lahore, start, end)
        data = data.fetch()
        combined_data = pd.concat([combined_data, data])

    averages = {}
    if 'tavg' in combined_data.columns:
        averages['tavg'] = combined_data['tavg'].mean()
    if 'prcp' in combined_data.columns:
        averages['prcp'] = combined_data['prcp'].mean()
    if 'rhum' in combined_data.columns:
        averages['rhum'] = combined_data['rhum'].mean()

    return averages

# Function to combine NPK recommendation and weather data to suggest specific crops
def combined_recommendation(n, p, k, target_year, start_month, start_day, end_month, end_day):
    npk_recommendation = get_plant_recommendation(n, p, k)
    weather_data = get_weather_data(target_year, start_month, start_day, end_month, end_day)

    weather_info = f"Average Temperature (\u00b0C): {weather_data.get('tavg', 'N/A')}\n"
    weather_info += f"Average Rainfall (mm): {weather_data.get('prcp', 'N/A')}\n"
    weather_info += f"Average Humidity (%): {weather_data.get('rhum', 'N/A')}\n"

    combined_info = f"Crop Recommendations based on NPK and Weather:\n\n{npk_recommendation}\n\nHistorical Weather Data:\n{weather_info}"

    return combined_info

# Button to get recommendations
if st.button("Get Recommendations"):
    recommendations = combined_recommendation(n_value, p_value, k_value, target_year, start_month, start_day, end_month, end_day)
    st.text_area("Recommendations (Crops & Weather)", recommendations, height=300)

st.write("---")
st.info("AgroEndure supports plant disease detection, water treatment, and budgeting to improve agricultural efficiency.")
