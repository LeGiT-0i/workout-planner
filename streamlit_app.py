# streamlit_app.py
import os
import json
import streamlit as st
import pandas as pd
from groq_client import generate_workout
from dotenv import load_dotenv

load_dotenv()

st.write("Loaded key:", os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Groq Workout Planner", layout="wide")

st.title("🏋️ Workout Planner (Groq + Streamlit)")

# Sidebar: user inputs
with st.sidebar.form("inputs"):
    st.header("Your profile")
    goal = st.selectbox("Goal", ["muscle_gain", "fat_loss", "strength", "endurance", "general_fitness"])
    experience = st.selectbox("Experience", ["beginner", "intermediate", "advanced"])
    days_per_week = st.slider("Days per week", 1, 7, 3)
    time_per_day = st.number_input("Minutes per day", min_value=10, max_value=180, value=45)
    equipment = st.multiselect("Available equipment", ["none", "dumbbells", "barbell", "bench", "pull-up bar", "kettlebell", "resistance bands"])
    injuries = st.text_area("Injuries or restrictions (optional)")
    submit = st.form_submit_button("Generate plan")

def build_prompt(goal, experience, days_per_week, time_per_day, equipment, injuries):
    prompt = f"""
You are a helpful and safe fitness coach. Produce a 7-day workout plan JSON for this user.
- goal: {goal}
- experience: {experience}
- days_per_week: {days_per_week}
- time_per_day_min: {time_per_day}
- equipment: {', '.join(equipment) if equipment else 'none'}
- injuries: {injuries if injuries else 'none'}

Output STRICT JSON only with keys: meta, plan (list of days with day number, focus, exercises), progression.
Each exercise entry: name, sets, reps, rest_sec, notes.
Only output JSON.
"""
    return prompt

if submit:
    prompt = build_prompt(goal, experience, days_per_week, time_per_day, equipment, injuries)
    st.info("Sending prompt to Groq AI...")
    try:
        res = generate_workout(prompt)
        raw_text = res["raw_text"]
        st.subheader("Raw AI response")
        st.code(raw_text, language="json")
        # Parse JSON - some LLMs include stray text; try to extract JSON.
        try:
            plan_json = json.loads(raw_text)
        except Exception:
            # fallback: try to find first '{' and last '}' substring
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            plan_json = json.loads(raw_text[start:end+1])

        # Show meta
        st.subheader("Plan summary")
        st.json(plan_json.get("meta", {}))

        # Show each day as a dataframe
        for day in plan_json.get("plan", []):
            st.markdown(f"### Day {day.get('day')} — {day.get('focus')}")
            df = pd.DataFrame(day.get("exercises", []))
            st.dataframe(df)

        st.subheader("Progression")
        st.write(plan_json.get("progression", ""))
    except Exception as e:
        st.error(f"Failed to generate plan: {e}")
