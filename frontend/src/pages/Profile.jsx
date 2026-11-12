
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getData, putData } from "../services/api";

function Profile() {

    const [profile, setProfile] = useState({
        first_name: "",
        last_name: ""
    });

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {

        async function loadProfile() {
            try {
                const data = await getData("profile");
                setProfile(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        loadProfile();

    }, []);

    function handleChange(e) {
        setProfile({
            ...profile,
            [e.target.name]: e.target.value
        });
    }

    async function handleSubmit(e) {
        e.preventDefault();

        setError("");
        setMessage("");

        try {

            const data = await putData("profile", {
                first_name: profile.first_name,
                last_name: profile.last_name
            });

            setProfile(data);
            setMessage(data.message);

        } catch (err) {
            setError(err.message);
        }
    }

    if (loading) {
        return <p>Loading profile...</p>;
    }

    return (
        <div className="container">

            <h2>My Profile</h2>

            <form onSubmit={handleSubmit}>

                <input
                    name="first_name"
                    value={profile.first_name}
                    placeholder="First Name"
                    className="form-control"
                    onChange={handleChange}
                />

                <br />

                <input
                    name="last_name"
                    value={profile.last_name}
                    placeholder="Last Name"
                    className="form-control"
                    onChange={handleChange}
                />

                <br />

                <button type="submit" className="btn btn-primary">
                    Update Profile
                </button>

            </form>

            {message && <p style={{ color: "green" }}>{message}</p>}

            {error && <p style={{ color: "red" }}>{error}</p>}

            <br />

            <Link to="/dashboard">Back to Dashboard</Link>

        </div>
    );
}

export default Profile;
