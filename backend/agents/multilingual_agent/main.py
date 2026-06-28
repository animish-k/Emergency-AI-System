import json
from multilingual_agent import MultilingualCAPAgent # type: ignore

DUMMY_CAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">

  <identifier>IND-NDMA-2026-FLOOD-CHN-001</identifier>
  <sender>ndma@gov.in</sender>
  <sent>2026-06-25T19:39:44+05:30</sent>
  <status>Actual</status>
  <msgType>Alert</msgType>
  <scope>Public</scope>

  <info>
    <language>en-IN</language>
    <category>Met</category>
    <event>Flood</event>
    <responseType>Evacuate</responseType>
    <urgency>Immediate</urgency>
    <severity>Extreme</severity>
    <certainty>Observed</certainty>
    <onset>2026-06-25T06:00:00+05:30</onset>
    <expires>2026-06-26T06:00:00+05:30</expires>
    <senderName>National Disaster Management Authority, India</senderName>

    <headline>EXTREME FLOOD WARNING — Immediate Evacuation Required in Chennai</headline>

    <description>
      Catastrophic flooding has been confirmed across multiple districts of Chennai
      following 72 hours of continuous heavy rainfall (120mm recorded).
      The Adyar and Cooum rivers have breached their banks.
      Water levels have risen to 9.2 metres, far exceeding the danger mark of 6.5 metres.
      Approximately 50,000 residents across Velachery, Adyar, Anna Nagar, and Tambaram
      are directly affected. Damage score: 92/100. Three bridges have been submerged.
      18 NDRF rescue boats and 50 rescue teams are currently deployed.
      10 ambulances and 5 medical units are on standby.
      50,000 food packets are being distributed. Rainfall expected for 18–24 more hours.
    </description>

    <instruction>
      ALL RESIDENTS IN AFFECTED ZONES MUST EVACUATE IMMEDIATELY.
      Do NOT attempt to cross flooded roads, bridges, or underpasses.
      Proceed to the nearest relief shelter by foot or rescue boat.
      Relief shelters: (1) Shelter A — Sri Ramachandra College, Porur (capacity 3000);
      (2) Shelter C — Zonal Office Ground, Velachery (capacity 1800).
      Carry only essential medicines, ID documents, and drinking water.
      Call 112 for emergency rescue. Helpline: 1800-425-1213 (Toll Free).
      Do NOT use electrical appliances. Do NOT enter basement areas.
    </instruction>

    <parameter><valueName>Rainfall</valueName><value>120</value></parameter>
    <parameter><valueName>Temperature</valueName><value>29</value></parameter>
    <parameter><valueName>SocialReports</valueName><value>340</value></parameter>
    <parameter><valueName>EmergencyCalls</valueName><value>120</value></parameter>
    <parameter><valueName>AffectedPopulation</valueName><value>50000</value></parameter>
    <parameter><valueName>DamageScore</valueName><value>92</value></parameter>
    <parameter><valueName>RescueTeams</valueName><value>50</value></parameter>
    <parameter><valueName>Ambulances</valueName><value>10</value></parameter>
    <parameter><valueName>MedicalUnits</valueName><value>5</value></parameter>
    <parameter><valueName>FoodPackets</valueName><value>50000</value></parameter>

    <contact>ndma-helpdesk@gov.in | +91-11-26701728</contact>

    <area>
      <areaDesc>Chennai District, Tamil Nadu — Velachery, Adyar, Anna Nagar, Tambaram</areaDesc>
    </area>
  </info>

</alert>"""


def main():
    # ── 1. Init agent ────────────────────────────────────────
    #  API key is read automatically from .env file
    agent = MultilingualCAPAgent(
        languages={
            "en": "English",
            "hi": "Hindi (हिन्दी)",
            "ta": "Tamil (தமிழ்)",
        }
    )

    # ── 2. Translate (pass real CAP XML from your agent here) ─
    result = agent.translate(DUMMY_CAP_XML)

    # ── 3. Print full JSON output ────────────────────────────
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # ── 4. Save to file ──────────────────────────────────────
    output_path = "cap_multilingual_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved → {output_path}")

    # ── 5. Pretty preview per language ──────────────────────
    print("\n" + "═" * 60)
    for code, msg in result["messages"].items():
        lang_name = agent.languages.get(code, code)
        print(f"\n🌐  {lang_name} [{code}]")
        print(f"    HEADLINE    : {msg.get('headline', '')}")
        print(f"    INSTRUCTION : {msg.get('instruction', '')[:120]}...")
        sms = msg.get('sms', '')
        print(f"    SMS ({len(sms)} chars): {sms}")
        print()


if __name__ == "__main__":
    main()
