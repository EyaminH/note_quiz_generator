from google import genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import io
import streamlit as st


#loading the env variable
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


#initializing a client
client = genai.Client(api_key=api_key)



#note generator
def note_generator(images):
    
    prompt = """Summarize the images in note format at max 100 words, 
    make sure to add necessary markdown to diffrentiate diffrent section"""
    
    response = client.models.generate_content(
        model = 'gemini-3-flash-preview',
        contents=[images, prompt]
    )
    
    return response.text


#audio transcription
def audio_transcription(text):
    speech = gTTS(text,lang='en', slow=False)
    audio_buffer = io.BytesIO()   # store space in ram
    speech.write_to_fp(audio_buffer)  # write that space in ram for the audio
    return audio_buffer


#quiz generator
def quiz_generator(images, difficulty):
    prompt = f"Generate 3 quizzes based on the {difficulty}, make sure to add necessary markdown to diffrentiate the options. Add correct answer too, after the quiz."
    response = client.models.generate_content(
        model = 'gemini-3-flash-preview',
        contents=[images, prompt]
    )
    
    return response.text
