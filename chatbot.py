import googlemaps
import google.generativeai as genai
import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

#API Keys
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#Configure APIs
genai.configure(api_key=GEMINI_API_KEY)
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

#Gemini Model Setup
model = genai.GenerativeModel("gemini-pro")

#For AI response
def chat_with_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
#To convert city name to coordinates
def get_coordinates(location):
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        return None
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return lat, lng

#Fetch top tourist places
def get_nearby_places(location):
    coords = get_coordinates(location)
    if not coords:
        return f"Sorry, I couldn't find that location: {location}"

    lat, lng = coords
    places_result = gmaps.places_nearby(
        location=(lat, lng),
        radius=5000,
        type='tourist_attraction'
    )

    if not places_result['results']:
        return f"Couldn't find tourist spots near {location}."

    places = [place['name'] for place in places_result['results'][:5]]
    return f"Top places to visit in {location}:\n- " + "\n- ".join(places)

def handle_user_query(message):
    travel_keywords = ["places", "visit", "tourist", "travel", "go to", "nearby", "location", "attractions"]
    if any(keyword in message.lower() for keyword in travel_keywords):
        return get_nearby_places(message)
    else:
        return chat_with_ai(message)
