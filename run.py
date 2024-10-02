import subprocess
import os

# Change to the 'app' directory
os.chdir('app')

# Run the Streamlit application
subprocess.run(['streamlit', 'run', 'Make_A_Workout.py'])
