import openai
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure this is set correctly in your .env file

# Function to get pH recommendation from OpenAI API
def get_ph_recommendation(ph_value):
    if ph_value < 7:
        # If acidic, recommend an organic process to make it neutral (Increase pH)
        prompt = f"""
        The water has a pH value of {ph_value}, which is acidic. 
        Please recommend organic procedures or filter-based solutions to raise the pH level and neutralize the acidity. 
        The goal is to bring the pH to 7 (neutral) without using chemicals. 
        You can include filters, natural substances, or other organic methods.
        """
    elif ph_value > 7:
        # If basic, recommend an organic process to make it neutral (Decrease pH)
        prompt = f"""
        The water has a pH value of {ph_value}, which is basic.
        Please recommend organic procedures or filter-based solutions to lower the pH level and neutralize the basicity.
        The goal is to bring the pH to 7 (neutral) without using chemicals.
        You can include filters, natural substances, or other organic methods.
        """
    else:
        # If the pH is already neutral
        return "The water has a neutral pH of 7. No treatment is necessary."

    # Use OpenAI to generate recommendations based on the prompt
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using the chat-based model
            messages=[
                {"role": "system", "content": "You are a helpful assistant for water treatment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Control the creativity of the response
            max_tokens=150  # Set the maximum number of tokens for the response
        )

        # Return the generated recommendation
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit interface
def streamlit_interface():
    st.title("Water pH Treatment Recommendation")
    st.write("Enter the pH value of your water to get recommendations for neutralizing it using organic methods or filter-based solutions.")

    # Input: pH value
    ph_value = st.number_input("Enter pH value", min_value=0.0, max_value=14.0, step=0.1)

    # Output: Recommendation
    if ph_value:
        recommendation = get_ph_recommendation(ph_value)
        st.text_area("Recommended Procedure", value=recommendation, height=150)

# Run the Streamlit app
if __name__ == "__main__":
    streamlit_interface()
