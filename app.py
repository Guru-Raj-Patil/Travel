from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from mistralai import Mistral

MISTRAL_API_KEY = "h3fo2GgugmzxHZtJbmKEqQI08zqaRCLU"
model = "mistral-large-latest"
import json

# Initialize Flask app
app = Flask(__name__)

# Get Mistral API key from environment variable (recommended for security)
# MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "your_mistral_api_key")

# Initialize Mistral client
client = Mistral(api_key=MISTRAL_API_KEY)

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes


@app.route("/api/generate-itinerary", methods=["POST"])
def generate_itinerary():

    try:
        # Get data from the request
        data = request.get_json()
        start_place = data.get("start", "")
        end_place = data.get("end", "")
        destination = data.get("destination", "")

        # Validate input
        if not all([start_place, end_place, destination]):
            return jsonify({"error": "Missing required parameters"}), 400

        # Generate prompt for Mixtral
        prompt = f"""Create a detailed travel itinerary from {start_place} to {destination} via {end_place} . 
        Include:
        - Estimated travel time
        - Key stops or points of interest along the way
        - Recommended mode of transportation
        - Estimated total distance
        - Approximate travel duration
        - Any unique local experiences or recommendations
        Format the response as a clear, easy-to-read strcutured markdown."""

        # Prepare messages for Mistral API
        messages = [{"role": "user", "content": prompt}]

        # Call Mistral API
        chat_response = client.chat.complete(model=model, messages=messages)

        # Extract the itinerary from the response
        itinerary_text = chat_response.choices[0].message.content.strip()

        # Try to parse as JSON, if not possible, return as is
        try:
            itinerary_json = json.loads(itinerary_text)
        except json.JSONDecodeError:
            itinerary_json = {"raw_itinerary": itinerary_text}

        return jsonify(itinerary_json)

    except Exception as e:
        print(f"Itinerary generation error: {str(e)}")
        return jsonify({"error": "Failed to generate itinerary"}), 500


@app.route("/api/destination/<dest_title>")
def get_destination_details(dest_title):
    # Convert URL-friendly format back to regular format
    dest_key = dest_title.lower().replace("-", "%20").replace(" ", "%20")

    # API key (consider moving this to an environment variable in a production setting)
    OLA_API_KEY = "tIsZPNT4JA0JyzmgaTLpJMcCziRjQEkpbWR3Yd4k"

    # Fetch places of interest
    poi_url = f"https://api.olamaps.io/places/v1/textsearch?input=Places%20of%20interest%20near%20{dest_key}&radius=5000&size=5&api_key={OLA_API_KEY}"

    try:
        # Fetch places of interest
        poi_response = requests.get(poi_url)
        poi_data = (
            poi_response.json()
            if poi_response.status_code == 200
            else {"predictions": []}
        )

        # Extract latitudes and longitudes from places of interest
        lat_lng_list = [
            (place["geometry"]["location"]["lat"], place["geometry"]["location"]["lng"])
            for place in poi_data.get("predictions", [])
        ]
        print(lat_lng_list)
        # Fetch restaurants for each POI location
        restaurants_data = []
        lat, lng = lat_lng_list[0]
        restaurant_url = f"https://api.olamaps.io/places/v1/nearbysearch?location={lat}%2C{lng}&types=restaurant&radius=10000&withCentroid=false&rankBy=popular&api_key={OLA_API_KEY}"
        restaurant_response = requests.get(restaurant_url)

        if restaurant_response.status_code == 200:
            restaurant_data = restaurant_response.json().get("predictions", [])
            restaurants_data.append(
                {"latitude": lat, "longitude": lng, "restaurants": restaurant_data}
            )
        print(restaurants_data)
        # Combine the results
        combined_details = {
            "places_of_interest": poi_data.get("predictions", []),
            "restaurants_nearby": restaurants_data,
        }

        # Optional: Write to a file for logging/debugging
        with open("destination_details.json", "w") as f:
            json.dump(combined_details, f, indent=4)

        return jsonify(combined_details)

    except Exception as e:
        print(f"Error fetching destination details: {str(e)}")
        return jsonify({"error": f"Error fetching details for {dest_title}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
