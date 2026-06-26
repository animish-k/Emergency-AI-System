from datetime import datetime

from services.weather_service import WeatherService
from services.usgs_service import USGSService

from agents.datacollection.sensors import SensorCollector
from agents.datacollection.socials import SocialCollector


class DataCollectionAgent:

    def __init__(self):

        self.weather = WeatherService()

        self.usgs = USGSService()

        self.sensor = SensorCollector()

        self.social = SocialCollector()

    def collect(
        self,
        location,
        disaster_type
    ):

        earthquake = self.usgs.get_latest_earthquake()

        weather_data = self.weather.get_weather(
    earthquake["latitude"],
    earthquake["longitude"]
)

        sensor_data = self.sensor.get_sensor_data(
            location
        )

        social_data = self.social.get_social_reports(
            location
        )

        final_data = {

            "location":
            earthquake["place"],

            "disaster_type":
            disaster_type,

            "earthquake_magnitude":
            earthquake["magnitude"],

            "earthquake_depth":
            earthquake["depth"],

            "latitude":
            earthquake["latitude"],

            "longitude":
            earthquake["longitude"],

            **weather_data,

            **sensor_data,

            **social_data,

            "emergency_calls":
            120,

            "timestamp":
            datetime.utcnow().isoformat()

        }

        return final_data