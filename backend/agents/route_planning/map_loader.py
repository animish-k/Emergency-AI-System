import osmnx as ox
import pandas as pd

from geopy.distance import geodesic


class MapLoader:

    def __init__(self):

        self.graph_cache = {}

        self.facility_cache = {}


    def load_graph(
        self,
        latitude,
        longitude
    ):

        key = (
            round(latitude, 2),
            round(longitude, 2)
        )

        if key in self.graph_cache:
            return self.graph_cache[key]

        distances = [

            30000,

            60000,

            100000,

            150000

        ]

        last_error = None

        for dist in distances:

            try:

                print(f"Trying road search radius: {dist} m")

                G = ox.graph_from_point(

                    (
                        latitude,
                        longitude
                    ),

                    dist=dist,

                    network_type="drive"

                )

                self.graph_cache[key] = G

                return G

            except Exception as e:

                print(f"No road network within {dist} m")

                last_error = e

        raise last_error
    def load_facilities(
    self,
    latitude,
    longitude
):

        key = (
            round(latitude, 2),
            round(longitude, 2)
        )

        if key in self.facility_cache:
            return self.facility_cache[key]

        print("Discovering facilities...")

        tags = {
            "amenity": [
                "hospital",
                "school",
                "community_centre"
            ]
        }

        facilities = ox.features_from_point(
            (
                latitude,
                longitude
            ),
            tags=tags,
            dist=30000
        )

        facilities = facilities.reset_index()

        FACILITIES = []

        for _, row in facilities.iterrows():

            try:

                name = row.get("name")

                if pd.isna(name):
                    continue

                amenity = row.get("amenity")

                geom = row.geometry

                if geom.geom_type == "Point":

                    lat = geom.y
                    lon = geom.x

                else:

                    center = geom.centroid

                    lat = center.y
                    lon = center.x

                FACILITIES.append({

                    "name": str(name),

                    "type": str(amenity),

                    "lat": float(lat),

                    "lon": float(lon)

                })

            except Exception:
                continue

        seen = set()
        unique = []

        for facility in FACILITIES:

            if facility["name"] not in seen:

                seen.add(facility["name"])
                unique.append(facility)

        for facility in unique:

            facility["straight_line_distance"] = geodesic(

                (
                    latitude,
                    longitude
                ),

                (
                    facility["lat"],
                    facility["lon"]
                )

            ).km

        unique.sort(
            key=lambda x: x["straight_line_distance"]
        )

        unique = unique[:50]

        self.facility_cache[key] = unique

        return unique