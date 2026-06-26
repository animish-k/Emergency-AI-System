import joblib
import os
import pandas as pd

class DamageAssessmentAgent:


    def __init__(self):

        BASE_DIR = os.path.dirname(__file__)

        MODEL_PATH = os.path.join(
            BASE_DIR,
            "model.pkl"
        )

        self.model = joblib.load(
            MODEL_PATH
        )

    def assess(self, data):

        X = pd.DataFrame([{

            "rainfall":
            data["rainfall"],

            "temperature":
            data["temperature"],

            "water_level":
            data["water_level"],

            "social_reports":
            data["social_reports"],

            "emergency_calls":
            data["emergency_calls"]

        }])

        base_score = float(
            self.model.predict(X)[0]
        )

        earthquake_bonus = 0

        if "earthquake_magnitude" in data:

            earthquake_bonus = (
                data["earthquake_magnitude"] * 15
            )

        score = min(
            base_score + earthquake_bonus,
            100
        )

        severity = self.get_severity(
            score
        )

        affected_population = int(
            score * 550
        )

        impact_zones = self.generate_impact_zones(
            severity,
            data["latitude"],
            data["longitude"]
        )

        return {

            "damage_score":
            round(score, 2),

            "severity":
            severity,

            "affected_population":
            affected_population,

            "impact_zones":
            impact_zones

        }

    def get_severity(
        self,
        score
    ):

        if score > 75:

            return "Extreme"

        elif score > 50:

            return "Severe"

        elif score > 25:

            return "Moderate"

        else:

            return "Low"

    def generate_impact_zones(
        self,
        severity,
        latitude,
        longitude
    ):

        center_lat = latitude
        center_lng = longitude

        if severity == "Low":

            return [

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 50000,
                    "risk": "extreme"
                },

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 100000,
                    "risk": "severe"
                },

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 150000,
                    "risk": "moderate"
                }

            ]

        elif severity == "Moderate":

            return [

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 100000,
                    "risk": "extreme"
                },

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 200000,
                    "risk": "severe"
                },

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 300000,
                    "risk": "moderate"
                }

            ]

        elif severity == "Severe":

            return [

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 150000,
                    "risk": "extreme"
                },

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 300000,
                    "risk": "severe"
                },

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 500000,
                    "risk": "moderate"
                }

            ]

        else:

            return [

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 200000,
                    "risk": "extreme"
                },

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 500000,
                    "risk": "severe"
                },

                {
                    "lat": center_lat,
                    "lng": center_lng,
                    "radius": 800000,
                    "risk": "moderate"
                }

            ]

