import os
import requests
from dotenv import load_dotenv

load_dotenv()


class PeopleSenseService:

    def __init__(self):

        self.api_key = os.getenv(
            "PEOPLESENSE_API_KEY"
        )

        self.base_url = (
            "https://w8bdwhaps0.execute-api.us-west-2.amazonaws.com/v1/occupancy"
        )

    def get_occupancy(self):

        headers = {
            "x-api-key": self.api_key
        }

        params = {
            "filter": "ALL"
        }

        response = requests.get(
            self.base_url,
            headers=headers,
            params=params
        )

        if response.status_code != 200:

            raise Exception(
                f"PeopleSense Error: {response.text}"
            )

        return response.json()
    def get_summary(self):

        response = self.get_occupancy()

        locations = response["data"]

        occupancies = []

        for item in locations:

            occ = item.get("Occupancy")

            if occ is not None:
                occupancies.append(occ)

        return {

            "total_locations":
            len(locations),

            "active_locations":
            len(occupancies),

            "average_occupancy":
            round(
                sum(occupancies) / len(occupancies),
                2
            ),

            "max_occupancy":
            max(occupancies),

            "crowded_locations":
            len(
                [
                    x
                    for x in occupancies
                    if x > 80
                ]
            )
        }