
import { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";

import { getData } from "../services/api";

function ProtectedRoute() {

    const [authenticated, setAuthenticated] = useState(null);

    useEffect(() => {

        let active = true;

        const verifyUser = async () => {

            try {

                // Get current user data to check if the user is authenticated
                const data = await getData("active_user");
                
                if (active && data.message) {
                    setAuthenticated(true);
                }

            } catch (error) {

                if (active) {
                    setAuthenticated(false);
                }

            }
        };

        verifyUser();

        return () => {
            active = false;
        };

    }, []);

    if (authenticated === null) {
        return (
            <div className="container text-center mt-5">
                <div className="spinner-border text-primary" />
                <p className="mt-2">
                    Checking authentication...
                </p>
            </div>
        );
    }

    return authenticated
        ? <Outlet />
        : <Navigate to="/login" replace />;
}

export default ProtectedRoute;
