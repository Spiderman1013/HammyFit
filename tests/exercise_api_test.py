import requests

# Get all exercises
response = requests.get('https://wger.de/api/v2/exercise')

if response.status_code == 200:
    exercises = response.json()
    # Filter exercises based on your criteria (e.g., compound, beginner-friendly)
    beginner_exercises = [exercise for exercise in exercises['results'] if exercise['level'] == 'beginner']
    print(beginner_exercises)
else:
    print("Error:", response.status_code)
