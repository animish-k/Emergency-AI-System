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

        self.model = joblib.load(MODEL_PATH)

    def assess(self,data):

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

        score = float(
            self.model.predict(X)[0]
        )

        severity = self.get_severity(score)

        affected = int(score * 550)

        return {

            "damage_score":
            round(score,2),

            "severity":
            severity,

            "affected_population":
            affected

        }

    def get_severity(self,score):

        if score > 85:
            return "Extreme"

        elif score > 60:
            return "Severe"

        elif score > 30:
            return "Moderate"

        else:
            return "Low"