import streamlit as st

# Function to display the homepage
def homepage():
    st.markdown("<h1 style='text-align: center;'>AgroEndure Dashboard</h1>", unsafe_allow_html=True)
    
    # Custom CSS for button styling
    st.markdown(
        """
        <style>
        .stButton>button {
            padding: 30px;
            font-size: 24px;
            font-weight: bold;
            background-color: white;
            color: #333;
            border: 3px solid #333;
            border-radius: 20px;
            width: 100%;
            height: 150px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #f0f0f0;
            border-color: #555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Creating layout with buttons linking to different pages
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🔧 Disease Detection"):
            st.switch_page("pages/Disease Detection.py")
    with col2:
        if st.button("🌱 pH Value"):
            st.switch_page("pages/PH Value.py")
    
    col3, col4 = st.columns(2, gap="large")
    with col3:
        if st.button("💧 Crop Budgeting"):
            st.switch_page("pages/Crop Budgeting.py")
    with col4:
        if st.button("🌾 Crop Recommendation"):
            st.switch_page("pages/Crop Recommendation.py")
    
    col5, col6 = st.columns(2, gap="large")
    with col5:
        if st.button("🌾 Specific Crop Recommendation"):
            st.switch_page("pages/Specific Crop Recommendation.py")
    with col6:
        if st.button("🗣️ Voice Assistant"):
            st.switch_page("pages/voiceans.py")
    
    col7, col8 = st.columns(2, gap="large")
    with col7:
        if st.button("🌦 Weather Forecast"):
            st.switch_page("pages/wheather.py")
    with col8:
        if st.button("💬 Marketplace"):
            st.switch_page("pages/chating.py")

# Initialize the homepage
homepage()
