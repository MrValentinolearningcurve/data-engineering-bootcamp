import requests


API_URL = "http://0.0.0.0:8000"
DATA = "events"
DATE = "2021-02-10"

response = requests.get(f"{API_URL}/{DATA}/?created_at={DATE}") ## define date
data = response.json()
for each in data:
    print(each["event_id"], each["event_type"])