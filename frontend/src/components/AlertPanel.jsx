function AlertPanel() {

    return (

        <div className="panel">

            <h3>Active Alerts</h3>

            <div className="alert critical">
                🔴 Earthquake Warning
            </div>

            <div className="alert warning">
                🟠 Aftershock Advisory
            </div>

            <div className="alert moderate">
                🟡 Tsunami Watch
            </div>

        </div>

    );

}

export default AlertPanel;