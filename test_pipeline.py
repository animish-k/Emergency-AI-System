from agents.datacollection.collector import DataCollectionAgent
from backend.agents.damage_assesment.predictor import DamageAssessmentAgent

# Initialize agents
collector = DataCollectionAgent()
damage_agent = DamageAssessmentAgent()

# Agent 1
data = collector.collect(
    location="Chennai",
    disaster_type="Flood"
)

print("\n===== AGENT 1 OUTPUT =====")
print(data)

# Agent 2
damage_result = damage_agent.assess(data)

print("\n===== AGENT 2 OUTPUT =====")
print(damage_result)