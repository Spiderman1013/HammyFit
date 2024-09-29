import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from st_on_hover_tabs import on_hover_tabs
import openai
from baml_src.baml_client.sync_client import b
from baml_src.baml_client.types import Exercises
from setPage import set_up_page
from dotenv import load_dotenv
import os
load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")


def get_json(experience_level, body_part, exercise_duration):
    data = b.ExtractExercises(experience_level, body_part, exercise_duration)
    return data
        
def get_exercises_from_api(experience_level, body_part, exercise_duration):
    try:
        #prompt = f"List exercise names for a {experience_level} level workout focusing on {body_part} with {exercise_duration} minutes to complete. Please only list the exercises nothing else. no modifications just the standardized name for the prompt. also each exercise should take atleast 3 minutes so dont give too many exercises. Also dont list any numbers just the exercises in a list. "
        # client = openai.OpenAI(
        #     # Defaults to os.environ.get("OPENAI_API_KEY")
        # )
        # chat_completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[{"role": "user", "content": prompt}]
        # )

        # exercises = chat_completion.choices[0].message.content.strip().split('\n')
        # return [exercise.strip() for exercise in exercises if exercise.strip()]
        list_of_exercises = get_json(str(experience_level), str(body_part), str(exercise_duration))
        return list_of_exercises
    except Exception as e:
        st.error(f"Error retrieving exercises: {e}")
        return []

set_up_page()

# Initialize session state for workout data
if 'workout_data' not in st.session_state:
    st.session_state['workout_data'] = {}

st.title("Configurations")

# Input for workout duration
duration_input = st.number_input("How many minutes do you want to work out?", step=5, min_value=5)

# Select box for experience level
experience_level = st.selectbox(
    "What is your fitness level?",
    ["Beginner", "Experienced", "Advanced"]
)

# Input for body part to work out
body_part = st.multiselect(
    "What is your fitness level?",
    ["Chest", "Shoulders","Back","Triceps","Biceps","Quads","Hamstrings","Calfs"]
)

# Save button to store workout data
col1, col2 = st.columns(2)

# Add the button in the first column (col1)
with col1:
    save_button = st.button("Save Workout Plan")

# You can also add other widgets or content in the second column (col2)
with col2:
    clear_button = st.button("Clear current plan")

if save_button:
    if not duration_input or not experience_level or not body_part:
        st.warning("Please fill in all the information above properly")
    else:
        st.session_state['workout_data'] = {
            'duration': duration_input,
            'experience_level': experience_level,
            'body_part': body_part
        }
        st.success("Workout plan saved successfully!")

        # Call the OpenAI API to get exercise names based on the user's input
        exercise_names = get_exercises_from_api(experience_level, body_part, duration_input)
        if exercise_names:
            st.subheader("Recommended Exercises:")
            st.session_state.exercise_names = exercise_names
            exercises = st.session_state.exercise_names.to_do
            for exercise in exercise_names.to_do:
                st.write(exercise)

if clear_button:
    st.session_state['workout_data'] = {}


# Display saved workout plan
if 'workout_data' in st.session_state and st.session_state['workout_data']:
    st.divider()
    left_column, right_column = st.columns([2, 2])  # Adjust the ratios as needed
    with left_column:
        st.subheader("Your Workout Plan:")
        st.write(f"**Duration:** {st.session_state['workout_data']['duration']} minutes")
        st.write(f"**Experience Level:** {st.session_state['workout_data']['experience_level']}")
        st.write(f"**Body Part:** {st.session_state['workout_data']['body_part']}")
        go_to_plan = st.button('Go to plan')
        if go_to_plan:
            st.switch_page('pages/2_Exercise_Plan.py')
    with right_column:
        st.image('hammy_gifs/happy_hammy.gif')
    st.divider()