import streamlit as st
import openai
import speech_recognition as sr
import os
import json
from dotenv import load_dotenv
from backend import generate_nishit_response

# Load API key
load_dotenv()
API_KEY = os.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Nishit's AI Voice Bot", page_icon="🎙️")
st.title("🎤 Talk to Nishit's AI Twin")
st.markdown("This is a voice bot trained to respond just like Nishit Dadhaniya. Ask a question using your mic or by typing below.")

# Session state for input_text
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

# Speech Recognition Function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source)
            st.success("Processing your voice input...")

            # Save temporary audio file
            temp_audio_path = "temp_audio.wav"
            with open(temp_audio_path, "wb") as f:
                f.write(audio_data.get_wav_data())

            # Whisper transcription
            with open(temp_audio_path, "rb") as audio_file:
                response = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            return response.text.strip()

        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the speech."
        except sr.RequestError:
            return "There was an error connecting to speech recognition services."

# Voice input button
if st.button("🎙️ Speak Now"):
    result = recognize_speech()
    if result:
        st.session_state["input_text"] = result

# Text input (no value= used!)
query = st.text_area("Or type your question here:", key="input_text", placeholder="e.g., What's your #1 superpower?")

# Get response button
if st.button("Get Response"):
    if not API_KEY:
        st.error("OpenAI API key not found. Add it in .env.")
    elif not query.strip():
        st.warning("Please provide a question first!")
    else:
        with st.spinner("Nishit is thinking..."):
            try:
                reply = generate_nishit_response(query, API_KEY)
                st.info(f"**You asked:** {query}")
                st.success(f"**Nishit replies:** {reply}")

                # Text-to-speech output
                safe_reply = json.dumps(reply)
                st.components.v1.html(f"""
                    <script>
                        const synth = window.speechSynthesis;
                        synth.cancel();
                        const utterance = new SpeechSynthesisUtterance({safe_reply});
                        utterance.lang = 'en-US';
                        utterance.pitch = 1;
                        utterance.rate = 1;
                        synth.speak(utterance);
                    </script>
                """, height=0)

            except Exception as e:
                st.error(f"An error occurred: {e}")
