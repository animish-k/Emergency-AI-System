import math
import requests


class PeopleSenseAgent:

    def __init__(self):

        self.url = (
            "https://w8bdwhaps0.execute-api.us-west-2.amazonaws.com/"
            "v1/occupancy?filter=ALL"
        )

        self.headers = {

            "x-api-key":
            "KplI1ustKlYvY14YfAm02XTdwMAEfmE46IHqbpQ5"

        }

    def haversine(

        self,

        lat1,

        lon1,

        lat2,

        lon2

    ):

        R = 6371

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)

        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (

            math.sin(dlat / 2) ** 2

            +

            math.cos(lat1)

            *

            math.cos(lat2)

            *

            math.sin(dlon / 2) ** 2

        )

        c = 2 * math.atan2(

            math.sqrt(a),

            math.sqrt(1 - a)

        )

        return R * c

    def nearby_transit(

        self,

        latitude,

        longitude

    ):

        try:

            response = requests.get(

                self.url,

                headers=self.headers,

                timeout=30

            )

            response.raise_for_status()

            occupancy_data = response.json()["data"]

        except:

            return []

        nearby = []

        for place in occupancy_data:

            lat = place.get("Latitude")
            lon = place.get("Longitude")

            if lat in [None, 0]:

                continue

            if lon in [None, 0]:

                continue

            distance = self.haversine(

                latitude,

                longitude,

                float(lat),

                float(lon)

            )

            if distance > 5:

                continue

            occupancy = place.get("Occupancy")

            max_occ = place.get("MaxOccupancy")

            percent = None

            if occupancy is not None:

                if max_occ and max_occ > 0:

                    percent = round(

                        occupancy / max_occ * 100,

                        1

                    )

                else:

                    percent = occupancy

            nearby.append({

                "name":

                place.get("GroupID")

                or

                place.get("PlaceID")

                or

                "Unknown",

                "distance":

                round(distance, 2),

                "occupancy_percent":

                percent

            })

        nearby.sort(

            key=lambda x:

            x["distance"]

        )

        return nearby[:5]