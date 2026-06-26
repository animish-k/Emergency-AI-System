import { useEffect, useState } from "react";
import api from "../services/api";

import {
    MapContainer,
    TileLayer,
    Marker,
    Popup,
    Circle,
    useMap
} from "react-leaflet";

import "leaflet/dist/leaflet.css";


function RecenterMap({ lat, lng }) {

    const map = useMap();

    useEffect(() => {

        map.setView(
            [lat, lng],
            8
        );

    }, [lat, lng, map]);

    return null;
}


function OccupancyMap({
    impactZones = []
}) {

    const [locations, setLocations] = useState([]);

    useEffect(() => {

        api.get("/occupancy-raw")

            .then((res) => {

                setLocations(res.data.data);

            })

            .catch((err) => {

                console.error(err);

            });

    }, []);
    console.log("Impact Zones:", impactZones);

    return (

        <div>

            <h2>PeopleSense Occupancy Map</h2>

            <MapContainer
                center={[37.5, -121.5]}
                zoom={6}
                style={{
                    height: "500px",
                    width: "100%"
                }}
            >

                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {impactZones.length > 0 && (

                    <RecenterMap
                        lat={impactZones[0].lat}
                        lng={impactZones[0].lng}
                    />

                )}

                {impactZones.map((zone, index) => {

                    let color = "yellow";

                    if (zone.risk === "severe")
                        color = "orange";

                    if (zone.risk === "extreme")
                        color = "red";

                    return (

                        <Circle
                            key={index}
                            center={[
                                zone.lat,
                                zone.lng
                            ]}
                            radius={zone.radius}
                            pathOptions={{
                                color: color,
                                fillColor: color,
                                fillOpacity: 0.35
                            }}
                        />

                    );

                })}

                {locations.map((location, index) => {

                    if (
                        !location.Latitude ||
                        !location.Longitude
                    )
                        return null;

                    return (

                        <Marker
                            key={index}
                            position={[
                                location.Latitude,
                                location.Longitude
                            ]}
                        >

                            <Popup>

                                <strong>
                                    {location.PlaceID}
                                </strong>

                                <br />

                                Occupancy:
                                {" "}
                                {location.Occupancy}

                                <br />

                                Capacity:
                                {" "}
                                {location.MaxOccupancy}

                            </Popup>

                        </Marker>

                    );

                })}

            </MapContainer>

        </div>

    );

}

export default OccupancyMap;