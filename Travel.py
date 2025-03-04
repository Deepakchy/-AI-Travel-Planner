import os
import streamlit as st
import requests
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI  
from langchain.schema import SystemMessage, HumanMessage
from deep_translator import GoogleTranslator
from datetime import datetime

# Set up the API key path dynamically
#base = os.path.dirname(os.path.abspath(__file__))
#file = os.path.join(base, "keys", "gemini.txt")  

# Load API key
#with open(file, "r") as f:
    #key = f.read().strip()
    #os.environ["GOOGLE_API_KEY"] = key  # Set environment variable

# Load API key from Streamlit Secrets
key = st.secrets["api"]["key"]

# Configure Google Generative AI
genai.configure(api_key=key)

# Initialize LangChain with Gemini
def get_travel_plan(source, destination, travel_mode, travel_preference, language, travel_date):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")  
    messages = [
        SystemMessage(content="You are an AI travel planner providing optimized travel plans."),
        HumanMessage(content=f"""
        Generate a detailed travel plan from {source} to {destination}.
        - Travel mode: {travel_mode}
        - Preference: {travel_preference}
        - Language: {language}
        - Date of travel: {travel_date}
        
        Also, check for ticket availability for trains and flights on the given date.
        Suggest related websites or apps where users can get more details.
        Include estimated travel time, cost, and comfort level.
        if any user put something outside source and destination name, politely decline.
        """)
    ]
    response = model.invoke(messages)
    return response.content

# Language translation
def translate_text(text, lang_code):
    return GoogleTranslator(source="auto", target=lang_code).translate(text)

lang_codes = {"English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te", "Maithili": "mai"}

# Streamlit UI
st.title("\U0001F30D AI Travel Planner")

source = st.text_input("Enter Source Location", placeholder="Enter starting location")
destination = st.text_input("Enter Destination", placeholder="Enter destination")
travel_mode = st.selectbox("Select Travel Mode", ["All", "Flight", "Train", "Bus", "Cab", "Bike"])
travel_preference = st.selectbox("Select Travel Preference", ["Any", "Budget", "Fastest", "Most Comfortable"])
travel_date = st.date_input("Select Travel Date", min_value=datetime.today())
language = st.selectbox("Select Language", ["English", "Hindi", "Tamil", "Telugu", "Maithili"])

if st.button("Plan My Travel"):
    if source and destination:
        travel_plan = get_travel_plan(source, destination, travel_mode, travel_preference, language, travel_date)
        if language in lang_codes:
            travel_plan = translate_text(travel_plan, lang_codes[language])
        st.write(travel_plan)
    else:
        st.warning("Please enter both source and destination!")
