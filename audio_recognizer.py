import streamlit as st
from audio_recorder_streamlit import audio_recorder
import io
import speech_recognition as sr

def record_and_recognize():
    # Record audio for a specific duration (e.g., 5 seconds)
    audio_bytes = audio_recorder()

    if audio_bytes:
        # Play the audio back to the user
        st.audio(audio_bytes, format="audio/wav")

        # Save the recorded audio to an in-memory file
        wav_io = io.BytesIO(audio_bytes)

        # Initialize the speech recognizer
        recognizer = sr.Recognizer()

        # Use the in-memory file as a source for speech recognition
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)  # Record all the data from the file

        # Perform speech recognition using Google Web Speech API
        try:
            st.write("Recognizing...")
            text = recognizer.recognize_google(audio)
            st.success(f"Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand the audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Web Speech API; {e}")

    return None

# Example of integrating the audio recognition with Streamlit
if st.button("Record and Recognize"):
    recognized_text = record_and_recognize()
    if recognized_text:
        st.write("Recognized text: ", recognized_text)