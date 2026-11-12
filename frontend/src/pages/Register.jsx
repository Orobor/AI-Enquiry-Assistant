
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { postData } from "../services/api";

function Register() {

    const navigate = useNavigate();
    
    const [form, setForm] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: ""
    });

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    function handleChange(e) {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    }

    async function handleSubmit(e) {
        e.preventDefault();

        setError("");
        setLoading(true);

        try {
            
            await postData("register", {
                first_name: form.first_name,
                last_name: form.last_name,
                email: form.email,
                password: form.password
            });
            navigate("/login", { replace: true });

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

                <h3 className="fw-bold text-dark">Create Account</h3>

                <p className="text-secondary">
                    Fill in the details to get started
                </p>

            </div>

            <div className="text-center mt-4">
                {error && <div className="alert alert-danger" role="alert"><strong>Error!</strong> {error}</div>}
            </div>

            <form onSubmit={handleSubmit}>

                <input
                    name="first_name"
                    placeholder="First Name"
                    value={form.first_name}
                    onChange={handleChange}
                    className="form-control"
                    required
                />

                <br />

                <input
                    name="last_name"
                    placeholder="Last Name"
                    value={form.last_name}
                    onChange={handleChange}
                    className="form-control"
                    required
                />

                <br />

                <input
                    name="email"
                    type="email"
                    placeholder="Email"
                    value={form.email}
                    onChange={handleChange}
                    className="form-control"
                    required
                />

                <br />

                <input
                    name="password"
                    type="password"
                    placeholder="Password"
                    value={form.password}
                    onChange={handleChange}
                    className="form-control"
                    required
                />

                <br />

                <button disabled={loading} className="btn btn-primary">
                    {loading ? "Registering..." : "Register"}
                </button>

            </form>

            <div className="text-center mt-4">

                <span className="text-secondary">
                    Already registered?  &nbsp;
                </span>

                <Link to="/login">Login</Link>

            </div>

        </div>
        </div>

            

    );
}

export default Register;
