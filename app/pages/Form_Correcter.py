import streamlit as st
import cv2
import threading
from playsound import playsound
import os
import time
import sys
from helpers.setPage import set_up_page
set_up_page()

cur_dir = os.getcwd()

help_dir  = os.path.abspath(os.path.join(cur_dir, 'helpers'))

# Add the grandparent directory to the system path
sys.path.append(help_dir)

from helpers.squats.utils import get_mediapipe_pose
from  helpers.squats.process_frame import ProcessFrame
from  helpers.squats.thresholds import get_thresholds_beginner, get_thresholds_pro


st.title('AI Fitness Trainer: Squats Analysis')

mode = st.radio('Select Mode', ['Beginner', 'Pro'], horizontal=True)

thresholds = None 
if mode == 'Beginner':
    thresholds = get_thresholds_beginner()
elif mode == 'Pro':
    thresholds = get_thresholds_pro()

upload_process_frame = ProcessFrame(thresholds=thresholds)

# Initialize pose detection
pose = get_mediapipe_pose()

stframe = st.empty()
stop_button = st.button("Stop")

# Set up the video capture from the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

ready = True

def play_sound(sound_to_play):
    for sound in sound_to_play:
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
        sound_file = os.path.join(parent_dir, 'assets', 'sounds', f'{sound}.mp3')
        st.write(sound_file)
        playsound(sound_file)
    time.sleep(3)
    global ready
    ready = True

if not cap.isOpened():
    st.error("Error: Could not open camera.")
else:
    st.sidebar.markdown("<p style='font-family:Helvetica; font-weight: bold; font-size: 16px;'>Live Camera Feed</p>", unsafe_allow_html=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Error: Could not read frame.")
            break

        # Convert frame from BGR to RGB before processing
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            st.error(f"OpenCV Error: {e}")
            break
        out_frame, sound_to_play = upload_process_frame.process(frame, pose)
        if sound_to_play is not None and ready:
            ready = False
            threading.Thread(target=play_sound, args=(sound_to_play,)).start()

        stframe.image(out_frame)
        # Optionally, you can add a stop button to break the loop
        if stop_button:
            break
cap.release()
stframe.empty()
