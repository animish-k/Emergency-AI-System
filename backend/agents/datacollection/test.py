from collector import DataCollectionAgent

agent = DataCollectionAgent()

result = agent.collect(

    location="Chennai",

    disaster_type="Flood"

)

print(result)