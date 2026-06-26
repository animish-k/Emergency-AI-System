import os
import requests

from dotenv import load_dotenv

load_dotenv()


class WeatherService:

    def __init__(self):

        self.api_key = os.getenv(
            "OPENWEATHER_API_KEY"
        )

    def get_weather(
        self,
        latitude,
        longitude
    ):

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={latitude}"
            f"&lon={longitude}"
            f"&appid={self.api_key}"
            "&units=metric"
        )

        response = requests.get(url)

        data = response.json()

        rainfall = 0

        if "rain" in data:

            rainfall = data["rain"].get(
                "1h",
                0
            )

        return {

            "temperature":
            data["main"]["temp"],

            "humidity":
            data["main"]["humidity"],

            "pressure":
            data["main"]["pressure"],

            "wind_speed":
            data["wind"]["speed"],

            "weather":
            data["weather"][0]["main"],

            "rainfall":
            rainfall

        }