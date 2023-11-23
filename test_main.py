import requests

# The URL where your Flask app is running, with the correct port
url = "http://localhost:8080/question"

# Parameters you want to pass to the GET request
params = {
    'lessonId': 1,
    'questionNumber': 1
}

# Make the GET request and print the response
response = requests.get(url, params=params)
print(response)
print(response.json())
