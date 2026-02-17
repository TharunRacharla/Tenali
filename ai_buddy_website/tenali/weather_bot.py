import os
import re
import requests

# Load OpenWeatherMap API key from environment
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    # Don't raise on import; the functions will return helpful messages when used
    print("Warning: OPENWEATHER_API_KEY not set. Weather queries will return an explanatory message.")

# Nominatim geocoding endpoint
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
# OpenWeatherMap API endpoint (use HTTPS)
OWM_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_coordinates(location):
    # Use the 'q' parameter for the location, 'format=json' to get the response in JSON
    params = {
        'q': location,
        'format': 'json',
        'addressdetails': 1,  # Get detailed address info (useful for cities)
        'limit': 1  # Limit to one result
    }

    headers = {
        'User-Agent': 'Tenali/1.0 (tharunracharla06442@gmail.com)'  # Set a User-Agent with your contact info
    }

    try:
        # Make the request with the User-Agent header
        response = requests.get(GEOCODE_URL, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check if the response contains results
        data = response.json()

        if data:  # If we have results
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return lat, lon
        else:
            return None, None  # No results found
    except requests.exceptions.RequestException as e:
        # Handle any request errors (e.g., network issues)
        print(f"Error while contacting the geocoding service: {e}")
        return None, None


def get_weather_info(user_input):
    # Extract city name using regex (supports "weather in <city>") or fallback
    m = re.search(r'in\s+(.+)$', user_input, re.IGNORECASE)
    if m:
        city = m.group(1).strip()
    else:
        # Try to remove the trigger word "weather" and use the rest
        city = user_input.lower().replace('weather', '').strip()
        if not city:
            return "Please specify a city, e.g., 'weather in London'."

    # Check API key
    if not API_KEY:
        return "Weather API key not configured. Please set OPENWEATHER_API_KEY in .env."

    lat, lon = get_coordinates(city)
    if not lat or not lon:
        return f"Sorry, I couldn't find coordinates for {city}."

    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(OWM_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        temperature = data.get('main', {}).get('temp')
        weather_description = data.get('weather', [{}])[0].get('description', 'N/A')
        humidity = data.get('main', {}).get('humidity', 'N/A')
        wind_speed = data.get('wind', {}).get('speed', 'N/A')

        weather_info = (
            f"Current weather in {city}:\n"
            f"Temperature: {temperature}°C\n"
            f"Condition: {weather_description.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
        return weather_info
    except requests.exceptions.HTTPError as e:
        # Common cause: invalid API key (401) or bad request
        try:
            status = response.status_code
        except Exception:
            status = 'unknown'
        if status == 401:
            return "Invalid OpenWeather API key. Please check OPENWEATHER_API_KEY."
        return f"Error fetching weather data (status {status}): {e}"
    except requests.exceptions.RequestException as e:
        return f"Network error while retrieving weather information: {e}"
