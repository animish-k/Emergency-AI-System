import { useEffect, useState } from "react";
import api from "../services/api";

function Resources() {
    const [resources, setResources] = useState(null);

    useEffect(() => {
        api.post("/pipeline", {
            location: "California",
            disaster_type: "Earthquake"
        }).then((res) => {
            setResources(res.data.resources);
        });
    }, []);

    if (!resources) return <h1>Loading...</h1>;

    const items = [
        { icon: "🚑", label: "Ambulances",    value: resources.ambulances },
        { icon: "👨‍⚕️", label: "Medical Teams", value: resources.medical_teams },
        { icon: "🚒", label: "Fire Trucks",   value: resources.fire_trucks },
        { icon: "👮", label: "Police Units",  value: resources.police_units },
        { icon: "🚁", label: "Helicopters",   value: resources.helicopters },
        { icon: "🏠", label: "Shelters",      value: resources.shelters },
    ];

    return (
        <div>
            <h1>Resource Allocation</h1>
            <p style={{ color: "#9ca3af", marginBottom: "24px" }}>
                Estimated people supported: {resources.estimated_people_supported?.toLocaleString()}
            </p>
            <div className="cards-grid">
                {items.map((item) => (
                    <div className="metric-card" key={item.label}>
                        <h3>{item.icon} {item.label}</h3>
                        <h1>{item.value}</h1>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Resources;
