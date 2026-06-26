import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import ImpactedAreas from "./pages/ImpactedAreas";
import Resources from "./pages/Resources";
import Alerts from "./pages/Alerts";
import "./App.css";

import Sidebar from "./components/Sidebar";

function App() {

    return (

        <BrowserRouter>

            <div className="app-layout">

                <Sidebar />

                <div className="content">

                    <Routes>

                        <Route
                            path="/"
                            element={<Dashboard />}
                        />

                        <Route
                            path="/impacted"
                            element={<ImpactedAreas />}
                        />

                        <Route
                            path="/resources"
                            element={<Resources />}
                        />

                        <Route
                            path="/alerts"
                            element={<Alerts />}
                        />

                    </Routes>

                </div>

            </div>

        </BrowserRouter>

    );

}

export default App;