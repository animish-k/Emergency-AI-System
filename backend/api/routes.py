from fastapi import APIRouter

from agents.datacollection.collector import (
    DataCollectionAgent
)

from agents.damage_assesment.predictor import (
    DamageAssessmentAgent
)
from agents.resource_allocation.resource_agent import (
    ResourceAllocationAgent
)
from agents.route_planning.route_agent import (
    RoutePlanningAgent
)
router = APIRouter()

collector = DataCollectionAgent()

damage_agent = DamageAssessmentAgent()

resource_agent = ResourceAllocationAgent()
route_agent = RoutePlanningAgent()

@router.get("/weather")
def get_weather(location: str = "Chennai"):

    data = collector.collect(
        location=location,
        disaster_type="Flood"
    )

    return {
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "rainfall": data["rainfall"]
    }

@router.get("/assess")
def assess_damage(location: str = "Chennai"):

    data = collector.collect(
        location=location,
        disaster_type="Flood"
    )

    return damage_agent.assess(data)

@router.post("/pipeline")
def run_pipeline(payload: dict):

    location = payload.get(
        "location",
        "Chennai"
    )

    disaster_type = payload.get(
        "disaster_type",
        "Flood"
    )

    data = collector.collect(
    location,
    disaster_type
)

    print("\n========== AGENT 1 ==========")
    print(data)
    print("=============================\n")

    result = damage_agent.assess(data)
    resources = resource_agent.allocate(result)
    route = route_agent.plan_route(

    data,

    result,

    resources

)
    return {
        "input": data,
        "assessment": result,
        "resources": resources,
        "route": route
    }


from services.peoplesense_service import (
    PeopleSenseService
)

peoplesense = PeopleSenseService()
@router.get("/occupancy-raw")
def get_occupancy():

    return peoplesense.get_occupancy()

@router.get("/occupancy-summary")
def occupancy_summary():

    return peoplesense.get_summary()