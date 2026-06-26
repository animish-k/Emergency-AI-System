from agents.datacollection.collector import DataCollectionAgent
from agents.damage_assesment.predictor import DamageAssessmentAgent

collector = DataCollectionAgent()
damage_agent = DamageAssessmentAgent()

data = collector.collect(
    location="USGS",
    disaster_type="Earthquake"
)

print("\n=== AGENT 1 OUTPUT ===")
print(data)

result = damage_agent.assess(data)

print("\n=== AGENT 2 OUTPUT ===")
print(result)