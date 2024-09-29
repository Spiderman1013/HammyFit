import streamlit as st
import openai  # Ensure you have the OpenAI library installed
import exerciseapi as exer
from dotenv import load_dotenv
from setPage import set_up_page
set_up_page()
load_dotenv()

client = openai.OpenAI(
        # Defaults to os.environ.get("OPENAI_API_KEY")
)

def get_exercise_description(exercise_name):
    """
    Given an exercise name, return a brief description of how to do the exercise with proper form.
    """
    prompt = f"Give a short and  brief description of how to perform a {exercise_name} with proper form."

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    exercises = chat_completion.choices[0].message.content.strip().split('\n')
    return "\n".join([exercise.strip() for exercise in exercises if exercise.strip()])

def component(exercise, index):
    with st.expander(f"**{exercise}**"):
        description = get_exercise_description(exercise)
        gif_url = exer.get_exercise_image(exercise)
        video_url = exer.get_exercise_video(exercise)
        if gif_url:
            st.image(gif_url, caption=exercise, use_column_width=True)
        if video_url:
            st.video(video_url)
        st.write(description)
        button = st.button(f"{index} Check my form")
        if button:
            st.switch_page('pages/Form_Correcter.py')
    # with c:
    #     st.write(f"**{exercise}**")

if "exercise_names" not in st.session_state:
    st.warning("Please enter a plan first before looking at your exercises")
else:
    exercises = st.session_state.exercise_names.to_do
    for index, exercise in enumerate(exercises):
        component(exercise, index)


