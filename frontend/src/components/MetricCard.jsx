function MetricCard({
    title,
    value,
    color
}) {

    return (

        <div
            className="metric-card"
            style={{
                borderTop: `4px solid ${color}`
            }}
        >

            <div className="metric-title">
                {title}
            </div>

            <div className="metric-value">
                {value}
            </div>

        </div>

    );

}

export default MetricCard;