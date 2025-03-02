import datetime
import requests
import subprocess
import spotipy
import os

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

bot_functions = {}

def register(func):
    bot_functions[func.__name__] = func
    return func

spotify_client_id = os.getenv("spotify_client_id")
spotify_secret = os.getenv("spotify_secret")
spotify_redirect_uri = os.getenv("spotify_redirect_uri")
spotify_scope = "user-modify-playback-state,user-read-playback-state"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                               client_secret=spotify_secret,
                                               redirect_uri=spotify_redirect_uri,
                                               scope=spotify_scope))

weather_api_key = os.getenv("weather_api_key")
weather_location = "Dallas"
weather_units = "imperial"

@register
def play_spotify_track_by_name(name: str):
    results = spotify.search(q=name, type='track', limit=1)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_uri = track['uri']

        devices = spotify.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            spotify.start_playback(device_id=device_id, uris=[track_uri])
        else:
            return "No Active Spotify Devices"
    else:
        return "Track Not Found"
    
    return f"Successfully Played {name}"

@register
def add_two_numbers(a: float, b: float) -> float:
    return float(a) + float(b)

@register
def subtract_two_numbers(a: float, b: float) -> float:
    return float(a) - float(b)

@register
def multiply_two_numbers(a: float, b: float) -> float:
    return float(a) * float(b)

@register
def divide_two_numbers(a: float, b: float) -> float:
    return float(a) / float(b)

@register
def current_time():
    return str(datetime.datetime.now())

@register
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
        
        return {
            "weather": weather, 
            "temperature": temperature
        }
    else:
        return "Weather Unknown"

@register
def launch_notepad():
    subprocess.run("notepad")
    return "Opened Notepad on Desktop"

@register
def launch_calculator():
    subprocess.run("calc")
    return "Opened Calculator on Desktop"

@register
def terminate_app():
    exit(0)

