from services.weather_service import WeatherService

service = WeatherService()

data = service.get_weather(
    "Chennai"
)

print(data)