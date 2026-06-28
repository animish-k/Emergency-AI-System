import requests


class USGSService:

    def get_latest_earthquake(self):

        url = (
            "https://earthquake.usgs.gov/"
            "earthquakes/feed/v1.0/"
            "summary/all_day.geojson"
        )

        response = requests.get(url)

        data = response.json()

        earthquake = data["features"][0]

        properties = earthquake["properties"]

        geometry = earthquake["geometry"]

        return {

            "place":
            properties["place"],

            "magnitude":
            properties["mag"],

            "time":
            properties["time"],

            "longitude":
            geometry["coordinates"][0],

            "latitude":
            geometry["coordinates"][1],

            "depth":
            geometry["coordinates"][2]

        }