import networkx as nx
import osmnx as ox

from .map_loader import MapLoader
from .peoplesense import PeopleSenseAgent


class RoutePlanningAgent:

    def __init__(self):

        self.loader = MapLoader()

        self.peoplesense = PeopleSenseAgent()

        self.facility_scores = {

            "hospital": 6,

            "community_centre": 4,

            "school": 3

        }

    def plan_route(

    self,

    data,

    assessment,

    resources

):

        user_lat = data["latitude"]
        user_lon = data["longitude"]

        print(f"Routing from: {user_lat}, {user_lon}")

        G = self.loader.load_graph(

            user_lat,

            user_lon

        )

        facilities = self.loader.load_facilities(

            user_lat,

            user_lon

        )

        origin = ox.distance.nearest_nodes(

            G,

            user_lon,

            user_lat

        )

        routes = []

        for facility in facilities:

            try:

                destination = ox.distance.nearest_nodes(

                    G,

                    facility["lon"],

                    facility["lat"]

                )

                route = nx.shortest_path(

                    G,

                    origin,

                    destination,

                    weight="length"

                )

                route_length = nx.shortest_path_length(

                    G,

                    origin,

                    destination,

                    weight="length"

                )

                distance_km = round(

                    route_length / 1000,

                    2

                )

                eta_min = round(

                    route_length / 500

                )

                coordinates = []

                for node in route:

                    coordinates.append({

                        "lat": G.nodes[node]["y"],

                        "lon": G.nodes[node]["x"]

                    })

                facility_score = self.facility_scores.get(

                    facility["type"],

                    1

                )

                distance_score = max(

                    0,

                    10 - distance_km

                )

                severity_bonus = 0

                if assessment["severity"] == "Extreme":

                    severity_bonus = 5

                elif assessment["severity"] == "Severe":

                    severity_bonus = 3

                elif assessment["severity"] == "Moderate":

                    severity_bonus = 1

                total_score = (

                    0.6 * distance_score

                    +

                    0.3 * facility_score

                    +

                    0.1 * severity_bonus

                )

                routes.append({

                    "facility": facility["name"],

                    "facility_type": facility["type"],

                    "distance_km": distance_km,

                    "eta_min": eta_min,

                    "score": round(total_score, 2),

                    "coordinates": coordinates

                })

            except Exception:

                continue

        try:

            nearby = self.peoplesense.nearby_transit(

                user_lat,

                user_lon

            )

        except Exception as e:

            print("PeopleSense Error:", e)

            nearby = []

        if len(routes) == 0:

            return {

                "recommended_route": None,

                "alternative_routes": [],

                "recommended_route_coordinates": [],

                "allocated_resources": resources,

                "severity": assessment["severity"],

                "affected_population": assessment["affected_population"],

                "nearby_transit": nearby

            }

        routes.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        best_route = routes[0]

        alternative_routes = []

        for route in routes[1:6]:

            alternative_routes.append({

                "facility": route["facility"],

                "facility_type": route["facility_type"],

                "distance_km": route["distance_km"],

                "eta_min": route["eta_min"],

                "score": route["score"]

            })

        return {

            "severity": assessment["severity"],

            "affected_population": assessment["affected_population"],

            "allocated_resources": resources,

            "recommended_route": {

                "facility": best_route["facility"],

                "facility_type": best_route["facility_type"],

                "distance_km": best_route["distance_km"],

                "eta_min": best_route["eta_min"],

                "score": best_route["score"]

            },

            "alternative_routes": alternative_routes,

            "recommended_route_coordinates": best_route["coordinates"],

            "nearby_transit": nearby

        }