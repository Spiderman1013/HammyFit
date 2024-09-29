import requests
from dotenv import load_dotenv
import os

load_dotenv()

auth_key = os.getenv("WGER_API_KEY")

def get_exercise_results(exercise_name):
    # Set up your variablesa
    url = "https://wger.de/api/v2/exercise/search/"
    headers = {
        "Authorization": auth_key,
        "Content-Type": "application/json"
    }
    params = {
        "language": "en",
        "term": exercise_name
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse JSON response

        exercises = data.get('suggestions', [])  # Access the 'data' field
        #print(exercises)

        # Print the first exercise
        return exercises[0] if isinstance(exercises, list) else exercises

    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_exercise_image(exercise_name):
    results = get_exercise_results(exercise_name)
    print(results)
    return "https://wger.de/" +str(results['data']['image'])

def get_exercise_video(exercise_name):
    results = get_exercise_results(exercise_name)

    base_id = results['data']['base_id']
    # Set up your variables
    url = "https://wger.de/api/v2/video/"
    headers = {
        "Authorization": auth_key,
        "Content-Type": "application/json"
    }
    params = {
        "exercise_base": base_id
    }

    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        print(data)
        results = data['results']
        if results:
            return results[0]['video']
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == '__main__':
    print(get_exercise_image('Barbell Squat'))
    print(get_exercise_video('Barbell Squat'))
