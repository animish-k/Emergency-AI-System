import os
from pathlib import Path
import uuid
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom




class CAPAlertAgent:

    def __init__(self):

        self.sender = "emergency-ai@gov.in"

        

    def generate_alert(self, data):

        alert = ET.Element("alert")

        ET.SubElement(alert,"identifier").text = str(uuid.uuid4())

        ET.SubElement(alert,"sender").text = self.sender

        ET.SubElement(
            alert,
            "sent"
        ).text = datetime.utcnow().isoformat()

        ET.SubElement(
            alert,
            "status"
        ).text = "Actual"

        ET.SubElement(
            alert,
            "msgType"
        ).text = "Alert"

        ET.SubElement(
            alert,
            "scope"
        ).text = "Public"

        info = ET.SubElement(
            alert,
            "info"
        )

        ET.SubElement(
            info,
            "category"
        ).text = self.get_category(
            data["disaster_type"]
        )

        ET.SubElement(
            info,
            "event"
        ).text = data["disaster_type"]

        ET.SubElement(
            info,
            "urgency"
        ).text = self.get_urgency(
            data["severity"]
        )

        ET.SubElement(
            info,
            "severity"
        ).text = data["severity"]

        ET.SubElement(
            info,
            "certainty"
        ).text = "Observed"

        ET.SubElement(
            info,
            "headline"
        ).text = self.generate_headline(
            data
        )

        ET.SubElement(
            info,
            "description"
        ).text = self.generate_description(
            data
        )
        parameters = {

            "EarthquakeMagnitude": data.get("earthquake_magnitude"),

            "EarthquakeDepth": data.get("earthquake_depth"),

            "Latitude": data.get("latitude"),

            "Longitude": data.get("longitude"),

            "Temperature": data.get("temperature"),

            "Humidity": data.get("humidity"),

            "Pressure": data.get("pressure"),

            "WindSpeed": data.get("wind_speed"),

            "Weather": data.get("weather"),

            "Rainfall": data.get("rainfall"),

            "WaterLevel": data.get("water_level"),

            "SocialReports": data.get("social_reports"),

            "EmergencyCalls": data.get("emergency_calls"),

            "DamageScore": data.get("damage_score"),

            "AffectedPopulation": data.get("affected_population")
        }

        for key, value in parameters.items():

            parameter = ET.SubElement(
                info,
                "parameter"
            )

            ET.SubElement(
                parameter,
                "valueName"
            ).text = str(key)

            ET.SubElement(
                parameter,
                "value"
            ).text = str(value)

        zones = ET.SubElement(info, "parameter")

        ET.SubElement(zones, "valueName").text = "ImpactZones"

        ET.SubElement(
            zones,
            "value"
        ).text = str(data.get("impact_zones"))

        ET.SubElement(
            info,
            "instruction"
        ).text = self.generate_instruction(
            data
        )

        area = ET.SubElement(
            info,
            "area"
        )

        ET.SubElement(
            area,
            "areaDesc"
        ).text = data["location"]

        return self.prettify_xml(alert)

    def get_category(
        self,
        disaster
    ):

        mapping = {

            "Flood": "Met",

            "Cyclone": "Met",

            "Earthquake": "Geo",

            "Landslide": "Geo",

            "Fire": "Fire"

        }

        return mapping.get(
            disaster,
            "Other"
        )

    def get_urgency(
        self,
        severity
    ):

        mapping = {

            "Extreme": "Immediate",

            "Severe": "Expected",

            "Moderate": "Expected",

            "Minor": "Future"

        }

        return mapping.get(
            severity,
            "Unknown"
        )

    def generate_headline(self, data):

        return (
            f"{data['disaster_type']} Alert | "
            f"Severity: {data['severity']} | "
            f"{data['location']}"
        )

    def generate_description(
        self,
        data
    ):

        return f"""
        Disaster Type: {data['disaster_type']}

        Location: {data['location']}

        Severity: {data['severity']}

        Damage Score: {data['damage_score']}

        Estimated Affected Population: {data['affected_population']}

        Weather Conditions:
        - Weather: {data['weather']}
        - Temperature: {data['temperature']} °C
        - Humidity: {data['humidity']} %
        - Pressure: {data['pressure']} hPa
        - Wind Speed: {data['wind_speed']} m/s
        - Rainfall: {data['rainfall']} mm

        Water Level:
        {data['water_level']} m

        Social Reports:
        {data['social_reports']}

        Emergency Calls:
        {data['emergency_calls']}
        """

    def generate_instruction(self, data):

        severity = data["severity"]

        if severity == "Extreme":
            return (
                "Immediate evacuation recommended. "
                "Follow directions issued by emergency authorities."
            )

        elif severity == "Severe":
            return (
                "Prepare to evacuate. "
                "Avoid affected areas."
            )

        elif severity == "Moderate":
            return (
                "Remain alert and monitor official updates."
            )

        else:
            return (
                "Continue monitoring the situation."
            )
        

    def prettify_xml(self, element):

        rough_string = ET.tostring(
            element,
            encoding="utf-8"
        )

        reparsed = minidom.parseString(
            rough_string
        )

        return reparsed.toprettyxml(
            indent="    "
        )
    

    def save_alert(self, xml_data):

        base_dir = os.path.dirname(os.path.abspath(__file__))

        alerts_folder = os.path.join(base_dir, "..", "..", "alerts")

        os.makedirs(alerts_folder, exist_ok=True)

        file_path = os.path.join(alerts_folder, "latest_alert.xml")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(xml_data)

        return file_path