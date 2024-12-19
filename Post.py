import requests
import json

url = "http://127.0.0.1:5000/api/users/"
data = {"name": "Alice Smith", "email": "alice@example.com"}
headers = {"Content-type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 201:
     print("User created successfully:")
     print(response.json())
else:
     print(f"Error creating user: {response.status_code} - {response.text}")