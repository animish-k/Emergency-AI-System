from fastapi import APIRouter

from agents.datacollection.collector import DataCollectionAgent
from agents.damage_assesment.predictor import DamageAssessmentAgent
from agents.resource_allocation.resource_agent import ResourceAllocationAgent
from agents.route_planning.route_agent import RoutePlanningAgent
from agents.alert_agent.cap_agent import CAPAlertAgent
from agents.edxl_agent.edxl_agent import run_edxl_agent
from services.peoplesense_service import PeopleSenseService

router = APIRouter()

collector = DataCollectionAgent()
damage_agent = DamageAssessmentAgent()
resource_agent = ResourceAllocationAgent()
route_agent = RoutePlanningAgent()
cap_agent = CAPAlertAgent()
peoplesense = PeopleSenseService()


@router.get("/weather")
def get_weather(location: str = "Chennai"):
    data = collector.collect(
        location=location,
        disaster_type="Flood"
    )
    return {
        "temperature": data["temperature"],
        "humidity": data.get("humidity"),
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
    location = payload.get("location", "Chennai")
    disaster_type = payload.get("disaster_type", "Flood")

    data = collector.collect(location, disaster_type)
    print("\n========== AGENT 1 ==========")
    print(data)

    assessment = damage_agent.assess(data)
    print("\n========== AGENT 2 ==========")
    print(assessment)

    resources = resource_agent.allocate(assessment)
    print("\n========== AGENT 3 ==========")
    print(resources)

    route = route_agent.plan_route(data, assessment, resources)
    print("\n========== AGENT 5 ==========")
    print(route)

    alert_input = {}
    alert_input.update(data)
    alert_input.update(assessment)
    alert_input.update(resources)
    cap_xml = cap_agent.generate_alert(alert_input)
    cap_agent.save_alert(cap_xml)
    print("\n========== AGENT 4 (CAP) ==========")
    print(cap_xml[:300])

    edxl_input = {
        "location": data["location"],
        "disaster_type": data["disaster_type"],
        "rainfall": data.get("rainfall", 0),
        "severity": assessment["severity"],
        "affected_population": assessment["affected_population"],
        "damage_score": assessment["damage_score"],
        "risk_level": assessment["severity"],
        "rescue_teams": resources.get("medical_teams", 0),
        "ambulances": resources.get("ambulances", 0),
        "medical_units": resources.get("medical_teams", 0),
        "food_packets": resources.get("shelters", 0) * 100,
        "evacuation_routes": (
            [route["recommended_route"]["facility"]]
            if route.get("recommended_route")
            else []
        ) + [
            r["facility"]
            for r in route.get("alternative_routes", [])[:2]
        ]
    }
    edxl_xml = run_edxl_agent(edxl_input)
    print("\n========== AGENT 6 (EDXL) ==========")
    print(edxl_xml[:300])

    return {
        "input": data,
        "assessment": assessment,
        "resources": resources,
        "route": route,
        "cap_alert": cap_xml,
        "edxl": edxl_xml,
    }


@router.get("/occupancy-raw")
def get_occupancy():
    return peoplesense.get_occupancy()


@router.get("/occupancy-summary")
def occupancy_summary():
    return peoplesense.get_summary()
