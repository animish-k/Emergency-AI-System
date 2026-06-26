from datetime import datetime

from services.weather_service import WeatherService

from agents.datacollection.sensors import SensorCollector
from agents.datacollection.socials import SocialCollector


class DataCollectionAgent:

    def __init__(self):

        self.weather = WeatherService()

        self.sensor = SensorCollector()

        self.social = SocialCollector()

    def collect(
        self,
        location,
        disaster_type
    ):

        weather_data = self.weather.get_weather(
            location
        )

        sensor_data = self.sensor.get_sensor_data(
            location
        )

        social_data = self.social.get_social_reports(
            location
        )

        final_data = {

            "location": location,

            "disaster_type": disaster_type,

            **weather_data,

            **sensor_data,

            **social_data,


            "emergency_calls": 120,

            "timestamp": datetime.utcnow().isoformat()

        }

        return final_data