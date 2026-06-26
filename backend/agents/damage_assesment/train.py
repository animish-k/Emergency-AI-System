import pandas as pd

from xgboost import XGBRegressor

import joblib

data = pd.read_csv("sample_data.csv")

X = data[[
    "rainfall",
    "temperature",
    "water_level",
    "social_reports",
    "emergency_calls"
]]

y = data["damage_score"]

model = XGBRegressor()

model.fit(X,y)

joblib.dump(
    model,
    "model.pkl"
)

print("Model Saved")