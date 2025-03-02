import os
import requests
from plugins.plugin_register import register

weather_api_key = os.getenv("weather_api_key")
weather_location = "Dallas"
weather_units = "imperial"

@register(plugin="weather")
def get_current_weather():
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": weather_location,
        "appid": weather_api_key,
        "units": weather_units
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather = data.get("weather", [{}])[0].get("description", "No description")
        temperature = data.get("main", {}).get("temp", "No temperature")
        return {"weather": weather, "temperature": temperature}
    else:
        return "Weather Unknown"
