import { useEffect, useState } from "react";
import api from "../services/api";

const SEVERITY_COLORS = {
    Extreme: "#ff4d4f",
    Severe: "#fa8c16",
    Moderate: "#fadb14",
    Low: "#52c41a",
};

function Alerts() {
    const [data, setData] = useState(null);

    useEffect(() => {
        api.post("/pipeline", {
            location: "California",
            disaster_type: "Earthquake"
        }).then((res) => {
            setData(res.data);
        });
    }, []);

    if (!data) return <h1>Loading...</h1>;

    const { assessment, resources, route } = data;
    const severityColor = SEVERITY_COLORS[assessment.severity] || "#fff";

    return (
        <div>
            <h1>Emergency Alerts</h1>

            <div className="metric-card" style={{
                borderLeft: `4px solid ${severityColor}`,
                marginBottom: "16px",
                alignItems: "flex-start"
            }}>
                <h3 style={{ color: severityColor }}>
                    🔴 {assessment.severity} {data.input.disaster_type} Alert
                </h3>
                <p><strong>Location:</strong> {data.input.location}</p>
                <p><strong>Damage Score:</strong> {assessment.damage_score} / 100</p>
                <p><strong>Affected Population:</strong> {assessment.affected_population?.toLocaleString()}</p>
                <p style={{ marginTop: "8px", color: "#9ca3af" }}>
                    {assessment.severity === "Extreme" && "Immediate evacuation recommended."}
                    {assessment.severity === "Severe" && "Prepare to evacuate. Avoid affected areas."}
                    {assessment.severity === "Moderate" && "Remain alert and monitor official updates."}
                    {assessment.severity === "Low" && "Continue monitoring the situation."}
                </p>
            </div>

            <div className="metric-card" style={{ marginBottom: "16px", alignItems: "flex-start" }}>
                <h3>🚑 Resource Deployment</h3>
                <p>{resources.ambulances} ambulances and {resources.medical_teams} medical teams dispatched.</p>
                <p>{resources.fire_trucks} fire trucks and {resources.police_units} police units deployed.</p>
                <p>{resources.shelters} shelters activated for {resources.estimated_people_supported?.toLocaleString()} people.</p>
            </div>

            {route?.nearby_transit?.length > 0 && (
                <div className="metric-card" style={{ marginBottom: "16px", alignItems: "flex-start" }}>
                    <h3>🟠 Nearby Occupancy (PeopleSense)</h3>
                    {route.nearby_transit.map((t, i) => (
                        <p key={i}>
                            <strong>{t.name}</strong> — {t.distance} km away,{" "}
                            {t.occupancy_percent !== null ? `${t.occupancy_percent}% occupied` : "occupancy unknown"}
                        </p>
                    ))}
                </div>
            )}

            {route?.recommended_route && (
                <div className="metric-card" style={{ alignItems: "flex-start" }}>
                    <h3>🟢 Evacuation Route Active</h3>
                    <p>
                        Recommended: <strong>{route.recommended_route.facility}</strong> ({route.recommended_route.facility_type})
                    </p>
                    <p>{route.recommended_route.distance_km} km — ETA {route.recommended_route.eta_min} min</p>
                </div>
            )}
        </div>
    );
}

export default Alerts;
