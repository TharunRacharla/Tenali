import requests

# Set your OpenWeatherMap API key
API_KEY = "ef4b63432237462678bcac31be6d05b9"

# Nominatim geocoding endpoint
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"

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
    # Extract city name (simple example assumes the city is in the input)
    city = user_input.split("in")[-1].strip()

    lat, lon = get_coordinates(city)
    
    if lat and lon:
        # Construct the weather API request using lat/lon
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()

            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_info = (
                f"Current weather in {city}:\n"
                f"Temperature: {temperature}°C\n"
                f"Condition: {weather_description.capitalize()}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s"
            )
            return weather_info
    return f"Sorry, I couldn't retrieve the weather information for {city}."
