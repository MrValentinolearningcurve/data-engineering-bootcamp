import json

import requests


if __name__ == "__main__":
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    data = response.json()
    print(data)

    try:
        with open("dogs.json", "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = {
            "data": []
        }

    existing_data["data"].append(data)

    with open("dogs.json", "w") as f:
        json.dump(existing_data, f)

    for i in existing_data["data"]:
        print(i)