class ResourceAllocationAgent:

    def allocate(self, assessment):

        severity = assessment.get(
            "severity",
            "Low"
        )

        affected = assessment.get(
            "affected_population",
            0
        )

        if severity == "Extreme":

            resources = {

                "ambulances": 30,

                "medical_teams": 20,

                "fire_trucks": 15,

                "police_units": 40,

                "helicopters": 5,

                "shelters": 25

            }

        elif severity == "Severe":

            resources = {

                "ambulances": 20,

                "medical_teams": 12,

                "fire_trucks": 10,

                "police_units": 25,

                "helicopters": 2,

                "shelters": 15

            }

        elif severity == "Moderate":

            resources = {

                "ambulances": 10,

                "medical_teams": 6,

                "fire_trucks": 5,

                "police_units": 15,

                "helicopters": 1,

                "shelters": 8

            }

        else:

            resources = {

                "ambulances": 4,

                "medical_teams": 2,

                "fire_trucks": 2,

                "police_units": 6,

                "helicopters": 0,

                "shelters": 3

            }

        resources["estimated_people_supported"] = affected

        return resources