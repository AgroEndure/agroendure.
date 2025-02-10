import base64
from dataclasses import dataclass
from typing import Literal
import random
import streamlit as st
import streamlit.components.v1 as components

# Function to encode images in Base64
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Load images (Ensure the correct paths)
ai_icon_base64 = encode_image("static/ai_icon.png")
user_icon_base64 = encode_image("static/user_icon.png")

def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

@dataclass
class Seller:
    name: str
    quantity: int
    price: int
    city: str
    contact: str

@dataclass
class Message:
    origin: Literal["human", "ai"]
    message: str

sellers_list = [
    "Ali Traders", "Green Fields Supply", "Agro Pakistan", "Organic Hub", "Fertile Land Suppliers"
]
cities = [
    "Lahore", "Karachi", "Islamabad", "Faisalabad", "Multan", "Rawalpindi", "Peshawar", "Quetta"
]

def generate_sellers(fertilizer_name):
    sellers = []
    for _ in range(random.randint(2, 3)):  # Ensure 2-3 sellers are generated
        sellers.append(Seller(
            name=random.choice(sellers_list),
            quantity=random.randint(10, 100),
            price=random.randint(500, 5000),
            city=random.choice(cities),
            contact=f"03{random.randint(0,9)}{random.randint(10000000, 99999999)}"
        ))
    return sellers

def on_click_callback():
    fertilizer_name = st.session_state.fertilizer_name
    sellers = generate_sellers(fertilizer_name)

    st.session_state.history.append(Message("human", fertilizer_name))
    
    st.markdown(f"### Sellers for {fertilizer_name}", unsafe_allow_html=True)

    for seller in sellers:
        with st.container():
            st.markdown(f"""
                <div style='border: 2px solid #007bff; border-radius: 10px; padding: 10px; margin-bottom: 10px; background-color: #f8f9fa;'>
                    <p><strong>🛒 Seller:</strong> {seller.name}</p>
                    <p><strong>🛆 Quantity:</strong> {seller.quantity} kg</p>
                    <p><strong>💰 Price:</strong> PKR {seller.price} per kg</p>
                    <p><strong>📍 City:</strong> {seller.city}</p>
                    <p><strong>📞 Contact:</strong> {seller.contact}</p>
                </div>
            """, unsafe_allow_html=True)

    st.session_state.history.append(Message("ai", f"Sellers for {fertilizer_name} are listed above."))

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []

initialize_session_state()
load_css()

st.title("Organic Fertilizer Seller Finder 🌱")

chat_placeholder = st.container()
prompt_placeholder = st.form("chat-form")

# Display Chat History with Base64 Icons
with chat_placeholder:
    for chat in st.session_state.history:
        icon_base64 = ai_icon_base64 if chat.origin == "ai" else user_icon_base64
        div = f"""
        <div class="chat-row {'' if chat.origin == 'ai' else 'row-reverse'}">
            <img class="chat-icon" src="data:image/png;base64,{icon_base64}" width=32 height=32>
            <div class="chat-bubble {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
                &#8203;{chat.message}
            </div>
        </div>
        """
        st.markdown(div, unsafe_allow_html=True)

    for _ in range(3):
        st.markdown("")

with prompt_placeholder:
    st.markdown("**Enter Organic Fertilizer Name**")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Fertilizer Name", 
        value="Compost", 
        label_visibility="collapsed", 
        key="fertilizer_name"
    )
    cols[1].form_submit_button(
        "Find Sellers", 
        type="primary", 
        on_click=on_click_callback
    )

components.html("""
<script>
const streamlitDoc = window.parent.document;
const buttons = Array.from(
    streamlitDoc.querySelectorAll('.stButton > button')
);
const submitButton = buttons.find(
    el => el.innerText === 'Find Sellers'
);

streamlitDoc.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        submitButton.click();
    }
});
</script>
""", height=0, width=0)
