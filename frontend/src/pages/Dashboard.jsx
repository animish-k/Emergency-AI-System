import { useEffect, useState } from "react";

import api from "../services/api";

import MetricCard from "../components/MetricCard";

import Topbar from "../components/Topbar";

import AlertPanel from "../components/AlertPanel";

import ResourcePanel from "../components/ResourcePanel";

import OccupancyMap from "./OccupancyMap";
import OccupancyStats from "../components/OccupancyStats";
import TimelinePanel from "../components/TimelinePanel";

function Dashboard() {

    const [data, setData] = useState(null);

    useEffect(() => {

        api.post("/pipeline", {
            location: "California",
            disaster_type: "Earthquake"
        })

        .then((res) => {

            setData(res.data);

        });

    }, []);

    if (!data)
        return <h1>Loading...</h1>;

    return (

        <div>

            <Topbar />

            <div className="cards-grid">

                <MetricCard
                    title="Severity"
                    value={data.assessment.severity}
                    color="#ff4d4f"
                />

                <MetricCard
                    title="Damage Score"
                    value={data.assessment.damage_score}
                    color="#fa8c16"
                />

                <MetricCard
                    title="Population"
                    value={data.assessment.affected_population}
                    color="#722ed1"
                />

                <MetricCard
                    title="Temperature"
                    value={data.input.temperature}
                    color="#1677ff"
                />

                <MetricCard
                    title="Humidity"
                    value={data.input.humidity}
                    color="#13c2c2"
                />

            </div>

            <div className="main-grid">

                <div className="map-panel">

                   <OccupancyMap
    impactZones={
        data.assessment.impact_zones
    }
/>

                </div>

                <div>

                    <AlertPanel />

                    <ResourcePanel />

                </div>
                <OccupancyStats />

    <TimelinePanel />

            </div>

        </div>

    );

}

export default Dashboard;