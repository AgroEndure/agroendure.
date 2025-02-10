import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
from gtts import gTTS
import os

# Function to set up OpenAI API key
def setup_openai_client(api_key):
    openai.api_key = api_key

# Function to transcribe Urdu audio
def transcribe_audio(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1", 
                file=audio_file,
                language="ur"
            )
        return transcript["text"].strip()  # Ensure proper extraction
    except Exception as e:
        return f"⚠️ خرابی ہوئی: {str(e)}"

# Function to get AI response in Urdu
def fetch_ai_response(input_text):
    if not input_text:  # Prevent empty requests
        return "معذرت! میں آپ کی بات نہیں سن سکا۔ براہ کرم دوبارہ بولیں۔"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106", 
            messages=[{"role": "user", "content": input_text}],
            temperature=0.7,
            max_tokens=4000
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ AI سے جواب حاصل کرنے میں مسئلہ ہوا: {str(e)}"

# Convert text to Urdu speech using Google TTS
def text_to_audio(text, audio_path):
    tts = gTTS(text=text, lang='ur')
    tts.save(audio_path)

# Streamlit UI
def main():
    st.sidebar.title("🔑 API KEY CONFIGURATION")
    api_key = st.sidebar.text_input("اپنا OpenAI API کلید درج کریں", type="password")
    
    st.title("🗣️ Aurora SpeakEasy - اردو")
    st.write("السلام علیکم! مجھ سے بات کرنے کے لئے نیچے ریکارڈنگ کا بٹن دبائیں۔")

    if api_key:
        setup_openai_client(api_key)
        recorded_audio = audio_recorder()

        if recorded_audio:
            audio_file = "audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(recorded_audio)

            st.write("🎙️ **ریکارڈ شدہ آڈیو پروسیسنگ میں ہے...**")
            
            transcribed_text = transcribe_audio(audio_file)
            
            if not transcribed_text or transcribed_text.startswith("⚠️"):  # Handle errors
                st.write(transcribed_text)
                return  

            st.write("📝 **تحریری متن:** ", transcribed_text)

            ai_response = fetch_ai_response(transcribed_text)

            response_audio_file = "audio_response.mp3"
            text_to_audio(ai_response, response_audio_file)
            
            st.audio(response_audio_file)
            st.write("🤖 **AI کا جواب:** ", ai_response)

if __name__ == "__main__":
    main()


