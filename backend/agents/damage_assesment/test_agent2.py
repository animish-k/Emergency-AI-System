from predictor import DamageAssessmentAgent

agent = DamageAssessmentAgent()

sample_input = {

    "rainfall": 130,

    "temperature": 28,

    "water_level": 8,

    "social_reports": 250,

    "emergency_calls": 100

}

result = agent.assess(sample_input)

print(result)