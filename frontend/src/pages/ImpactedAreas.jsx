import { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import api from "../services/api";

const RISK_COLORS = {
    extreme: "red",
    severe: "orange",
    moderate: "yellow",
};

function metrestoRadius(metres) {
    return Math.min(Math.max(metres / 10000, 10), 60);
}

function ImpactedAreas() {
    const [assessment, setAssessment] = useState(null);
    const [route, setRoute] = useState(null);

    useEffect(() => {
        api.post("/pipeline", {
            location: "California",
            disaster_type: "Earthquake"
        }).then((res) => {
            setAssessment(res.data.assessment);
            setRoute(res.data.route);
        });
    }, []);

    if (!assessment) return <h1>Loading...</h1>;

    const zones = assessment.impact_zones || [];
    const center = zones.length > 0
        ? [zones[0].lat, zones[0].lng]
        : [37.5, -121.5];

    const routeCoords = route?.recommended_route_coordinates?.map(
        (c) => [c.lat, c.lon]
    ) || [];

    return (
        <div>
            <h1>Earthquake Impact Zones</h1>

            {route?.recommended_route && (
                <div className="panel" style={{ marginBottom: "16px" }}>
                    <h3>Recommended Evacuation Route</h3>
                    <p>
                        <strong>Destination:</strong> {route.recommended_route.facility} ({route.recommended_route.facility_type})
                    </p>
                    <p>
                        <strong>Distance:</strong> {route.recommended_route.distance_km} km &nbsp;|&nbsp;
                        <strong>ETA:</strong> {route.recommended_route.eta_min} min
                    </p>
                    {route.alternative_routes?.length > 0 && (
                        <>
                            <h4>Alternative Routes</h4>
                            {route.alternative_routes.map((r, i) => (
                                <p key={i}>
                                    {i + 1}. {r.facility} — {r.distance_km} km ({r.eta_min} min)
                                </p>
                            ))}
                        </>
                    )}
                </div>
            )}

            <MapContainer
                center={center}
                zoom={6}
                style={{ height: "600px", width: "100%" }}
            >
                <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

                {zones.map((zone, idx) => (
                    <CircleMarker
                        key={idx}
                        center={[zone.lat, zone.lng]}
                        radius={metrestoRadius(zone.radius)}
                        pathOptions={{
                            color: RISK_COLORS[zone.risk] || "gray",
                            fillOpacity: 0.3
                        }}
                    >
                        <Popup>
                            Risk Level: <strong>{zone.risk}</strong><br />
                            Radius: {(zone.radius / 1000).toFixed(0)} km
                        </Popup>
                    </CircleMarker>
                ))}

                {routeCoords.length > 1 && (
                    <Polyline
                        positions={routeCoords}
                        pathOptions={{ color: "cyan", weight: 3 }}
                    />
                )}
            </MapContainer>
        </div>
    );
}

export default ImpactedAreas;
