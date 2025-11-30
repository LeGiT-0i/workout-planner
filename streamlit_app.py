# streamlit_app.py
from dotenv import load_dotenv
load_dotenv()  # Must be first to load .env

import streamlit as st
import pandas as pd
import json
from groq_client import generate_workout

st.set_page_config(page_title="Groq Workout Planner", layout="wide")
st.title("🏋️ Workout Planner (Groq + Streamlit)")

# Sidebar: user input
with st.sidebar.form("user_inputs"):
    st.header("Your Profile")
    goal = st.selectbox("Goal", ["muscle_gain", "fat_loss", "strength", "endurance", "general_fitness"])
    experience = st.selectbox("Experience", ["beginner", "intermediate", "advanced"])
    days_per_week = st.slider("Days per week", 1, 7, 3)
    time_per_day = st.number_input("Minutes per day", min_value=10, max_value=180, value=45)
    equipment = st.multiselect("Available equipment", ["none", "dumbbells", "barbell", "bench", "pull-up bar", "kettlebell", "resistance bands"])
    injuries = st.text_area("Injuries or restrictions (optional)")
    submit = st.form_submit_button("Generate Workout Plan")

def build_prompt(goal, experience, days, time, equipment, injuries):
    return f"""
You are a helpful and safe fitness coach. Create a 7-day workout plan in strict JSON for a user.
- goal: {goal}
- experience: {experience}
- days_per_week: {days}
- time_per_day_min: {time}
- equipment: {', '.join(equipment) if equipment else 'none'}
- injuries: {injuries if injuries else 'none'}

Output STRICT JSON with keys:
- meta: dictionary with goal, experience, days_per_week, notes
- plan: list of 7 days, each day with day number, focus, exercises
    - each exercise: name, sets, reps, rest_sec, notes
- progression: short instructions on how to progress each week
Only output JSON.
"""

if submit:
    prompt = build_prompt(goal, experience, days_per_week, time_per_day, equipment, injuries)
    st.info("Generating workout plan from Groq AI...")

    try:
        res = generate_workout(prompt)
        raw_text = res["raw_text"]
        st.subheader("Raw AI JSON Output")
        st.code(raw_text, language="json")

        # Attempt to parse JSON
        try:
            plan_json = json.loads(raw_text)
        except Exception:
            start = raw_text.find("{")
            end = raw_text.rfind("}")
            plan_json = json.loads(raw_text[start:end+1])

        # Show meta
        st.subheader("Plan Summary")
        st.json(plan_json.get("meta", {}))

        # Show each day
        for day in plan_json.get("plan", []):
            st.markdown(f"### Day {day.get('day')} — {day.get('focus')}")
            df = pd.DataFrame(day.get("exercises", []))
            st.dataframe(df)

        st.subheader("Progression")
        st.write(plan_json.get("progression", ""))

    except Exception as e:
        st.error(f"Failed to generate plan: {e}")
