class ResourceAllocationAgent:

    def allocate(self, assessment):

        severity = assessment.get("severity", "Medium")

        if severity == "High":
            return {
                "ambulances": 10,
                "medical_teams": 5,
                "fire_trucks": 4,
                "police_units": 12
            }

        elif severity == "Medium":
            return {
                "ambulances": 6,
                "medical_teams": 3,
                "fire_trucks": 2,
                "police_units": 8
            }

        else:
            return {
                "ambulances": 3,
                "medical_teams": 2,
                "fire_trucks": 1,
                "police_units": 4
            }