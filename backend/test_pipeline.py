from agents.datacollection.collector import DataCollectionAgent
from agents.damage_assesment.predictor import DamageAssessmentAgent
from agents.alert_agent.cap_agent import CAPAlertAgent

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

# -----------------------------
# Merge Agent Outputs
# -----------------------------
alert_input = {}

alert_input.update(data)
alert_input.update(result)

cap_agent = CAPAlertAgent()
cap_xml = cap_agent.generate_alert(alert_input)
path = cap_agent.save_alert(cap_xml)

print(f"Saved alert to {path}")
print("\n=== ALERT AGENT OUTPUT ===")
print(cap_xml)