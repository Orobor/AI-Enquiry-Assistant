import './assets/bootstrap/bootstrap.min.css'
import './assets/bootstrap/bootstrap.bundle.min.js'

import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {

    return (

        <BrowserRouter>

                <Routes>
                    
                     {/* Public routes */}
                     
                    <Route
                        path="/"
                        element={<Navigate to="/dashboard" replace />}
                    />

                    <Route
                        path="/login"
                        element={<Login />}
                    />

                    <Route
                        path="/register"
                        element={<Register />}
                    />

                    <Route
                        path="*"
                        element={<Navigate to="/" replace />}
                    />

                    {/* Protected routes */}

                    <Route element={<ProtectedRoute />}>

                        <Route
                            path="/dashboard"
                            element={<Dashboard />}
                        />

                        <Route
                            path="/profile"
                            element={<Profile />}
                        />

                    </Route>

                </Routes>

        </BrowserRouter>
    );
}

export default App;
