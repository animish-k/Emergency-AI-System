import {
    MapContainer,
    TileLayer,
    CircleMarker,
    Popup
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

function ImpactedAreas() {

    const zones = [

        {
            lat: 37.7749,
            lng: -122.4194,
            level: "High",
            color: "red"
        },

        {
            lat: 37.3382,
            lng: -121.8863,
            level: "Moderate",
            color: "orange"
        },

        {
            lat: 38.5816,
            lng: -121.4944,
            level: "Low",
            color: "green"
        }

    ];

    return (

        <div>

            <h1>Earthquake Impact Zones</h1>

            <MapContainer
                center={[37.5, -121.5]}
                zoom={6}
                style={{
                    height: "700px",
                    width: "100%"
                }}
            >

                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {

                    zones.map((zone, idx) => (

                        <CircleMarker
                            key={idx}
                            center={[
                                zone.lat,
                                zone.lng
                            ]}
                            radius={30}
                            pathOptions={{
                                color: zone.color
                            }}
                        >

                            <Popup>

                                Earthquake Zone

                                <br />

                                Severity:
                                {" "}
                                {zone.level}

                            </Popup>

                        </CircleMarker>

                    ))

                }

            </MapContainer>

        </div>

    );

}

export default ImpactedAreas;