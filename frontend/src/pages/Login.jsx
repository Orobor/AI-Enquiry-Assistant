
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { postData } from "../services/api";

function Login() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e) {
        e.preventDefault();

        setError("");
        setLoading(true);
        
        try {
            
            // call api with endpoint 'login' to login user
            await postData("login", {
                username : username,
                password : password,
            });
            
            navigate("/dashboard", { replace: true });

        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="container-fluid min-vh-100 d-flex justify-content-center align-items-center py-5">
        <div className="card border-0 shadow-lg rounded-4 w-100" style={{ maxWidth: "420px", padding: "30px" }}>
            
            <div className="text-center mb-2">

                    <h2 className="fw-bold text-dark">Welcome Back!</h2>

                    <p className="text-secondary">
                        Login to access your account
                    </p>

            </div>

            <form onSubmit={handleSubmit}>

                <input
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                    placeholder="Email"
                    className="form-control"
                    required
                />

                <br />

                <input
                    type="password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    placeholder="Password"
                    className="form-control"
                    required
                />

                <br />

                <button disabled={loading}
                    className="btn btn-primary btn-lg w-100 fw-semibold shadow-sm">
                        {loading ? "Logging in..." : "Login"}
                    <i className="bi bi-arrow-right ms-2"></i>
                </button>

                <div className="text-center mt-4">
                    {error && <div className="alert alert-danger" role="alert"><strong>Error!</strong> {error}</div>}
                </div>

            </form>

            <div className="d-flex align-items-center my-4">

                    <hr className="flex-grow-1" />

                    <span className="px-3 text-secondary small">
                        OR CONTINUE WITH
                    </span>

                    <hr className="flex-grow-1" />

                </div>

                <div className="row g-2">

                    <div className="col-6">
                        <button className="btn btn-outline-secondary w-100">
                            <i className="bi bi-google me-2"></i>
                            Google
                        </button>
                    </div>

                    <div className="col-6">
                        <button className="btn btn-outline-secondary w-100">
                            <i className="bi bi-github me-2"></i>
                            GitHub
                        </button>
                    </div>

                </div>

            <div className="text-center mt-4">

                    <span className="text-secondary">
                        Don't have an account? &nbsp;
                    </span>

                    <Link to="/register">Register</Link>

            </div>

        </div>
        </div>
        
    );
}

export default Login;
