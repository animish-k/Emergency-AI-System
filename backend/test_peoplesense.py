from services.peoplesense_service import PeopleSenseService

service = PeopleSenseService()

data = service.get_occupancy()

print(data)