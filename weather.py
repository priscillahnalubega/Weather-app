import argparse
from configparser import ConfigParser
import requests

def _get_api_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["api_key"]

def fetch_weather_data(city, imperial_units, api_key):
    units = "imperial" if imperial_units else "metric"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print("Error fetching weather data.")
        return None

def read_user_cli_args():
    parser = argparse.ArgumentParser(
        description="Get weather and temperature information for a city"
    )
    parser.add_argument(
        "city", nargs="+", type=str, help="Enter the city name(s)"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="Display the temperature in imperial units",
    )
    return parser.parse_args()

if __name__ == "__main__":
    user_args = read_user_cli_args()
    api_key = _get_api_key()

    if api_key:
        for city in user_args.city:
            weather_data = fetch_weather_data(city, user_args.imperial, api_key)

            if weather_data:
                temperature = weather_data["main"]["temp"]
                unit = "Fahrenheit" if user_args.imperial else "Celsius"

                print(f"Weather in {city}:")
                print(f"Temperature: {temperature} {unit}")
                print(f"Description: {weather_data['weather'][0]['description']}\n")
    else:
        print("API key not found in secrets.ini.")
