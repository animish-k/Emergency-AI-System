function Alerts() {

    return (

        <div>

            <h1>Emergency Alerts</h1>

            <div className="metric-card">

                <h3>🔴 Flood Warning</h3>

                <p>
                    High flood risk detected.
                </p>

            </div>

            <br />

            <div className="metric-card">

                <h3>🟠 Occupancy Alert</h3>

                <p>
                    PeopleSense reports crowd density above threshold.
                </p>

            </div>

        </div>

    );

}

export default Alerts;