import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a budget for the given crop
def generate_budget(crop_name):
    prompt = f"""
    Based on current agricultural data for Pakistan in 2024, generate a budget breakdown for the following crop: {crop_name}.
    Include the following details:
    1. Estimated seed cost for 1 acre in PKR
    2. Estimated fertilizer cost for 1 acre in PKR
    3. Expected profit margin based on an 8-10% increase from previous year prices
    4. Total cost and expected profit per acre
    5. Total revenue after profit per acre
    Please give the results in a clear, structured format, like:
    - Seed Cost: [Amount] PKR
    - Fertilizer Cost: [Amount] PKR
    - Profit Margin: [Percentage]%
    - Profit: [Amount] PKR
    - Total Revenue: [Amount] PKR
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that helps farmers generate crop budgets."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        budget_details = response.choices[0].message['content'].strip()
        return budget_details
    except Exception as e:
        return f"Error generating budget: {e}"

# Function to calculate the total profit and revenue per acre
def calculate_final_budget(seed_cost, fertilizer_cost, profit_margin):
    total_cost = seed_cost + fertilizer_cost
    profit = total_cost * (profit_margin / 100)
    total_revenue = total_cost + profit
    return total_cost, profit, total_revenue

# Streamlit app UI
st.title("Crop Budget Generator for Pakistan (2024)")

crop_name = st.text_input("Enter the Crop Name", placeholder="e.g., Wheat, Rice, Corn")

if st.button("Generate Budget"):
    if crop_name.strip():
        # Generate budget from OpenAI
        budget_response = generate_budget(crop_name)
        st.subheader("Budget Breakdown from AI:")
        st.text(budget_response)

        # Example fixed values (for demo purposes; these can be parsed from the AI output)
        seed_cost = 12000  # Example value
        fertilizer_cost = 20000  # Example value
        profit_margin = 10  # Example value (10%)

        # Calculate the final budget values
        total_cost, profit, total_revenue = calculate_final_budget(seed_cost, fertilizer_cost, profit_margin)

        # Display calculated results
        st.subheader("Calculated Budget Summary:")
        st.json({
            "Seed Cost (PKR)": seed_cost,
            "Fertilizer Cost (PKR)": fertilizer_cost,
            "Profit Margin (%)": profit_margin,
            "Total Cost (PKR)": total_cost,
            "Profit (PKR)": profit,
            "Total Revenue (PKR)": total_revenue
        })
    else:
        st.warning("Please enter a crop name.")
