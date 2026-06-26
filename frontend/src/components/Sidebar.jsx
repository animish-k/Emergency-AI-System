import { Link } from "react-router-dom";

function Sidebar() {

    return (

        <div className="sidebar">

            <h2>Emergency AI</h2>

            <Link to="/">Dashboard</Link>

            <Link to="/impacted">
                Impacted Areas
            </Link>

            <Link to="/resources">
                Resources
            </Link>

            <Link to="/alerts">
                Alerts
            </Link>

        </div>

    );

}

export default Sidebar;