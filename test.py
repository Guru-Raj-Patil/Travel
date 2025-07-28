# import requests

# url = "https://api.makcorps.com/city"
# params = {
#     "cityid": "60763",
#     "pagination": "0",
#     "cur": "USD",
#     "rooms": "1",
#     "adults": "2",
#     "checkin": "2024-12-25",
#     "checkout": "2024-12-26",
#     "api_key": "6739d80fee828d915fb4e154",
# }

# response = requests.get(url, params=params)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse JSON response
#     json_data = response.json()

#     # Print or use the parsed JSON data
#     print(json_data)
# else:
#     # Print an error message if the request was not successful
#     print(f"Error: {response.status_code}, {response.text}")

import requests
import json

url = "https://api.makcorps.com/mapping"
params = {"api_key": "6739d80fee828d915fb4e154", "name": "Ziro Valley India"}

response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON response
    json_data = response.json()

    # Print or use the parsed JSON data
    print(json_data)

    # write to a file
    with open("data.json", "w") as f:
        json.dump(json_data, f, indent=4)
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code}, {response.text}")

