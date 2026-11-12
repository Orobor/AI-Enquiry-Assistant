
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ChatWidget from "./ChatWidget";
import { getData, postData } from "../services/api";

function Dashboard() {
    const navigate = useNavigate();

    const [user, setUser] = useState(null);

    useEffect(() => {
        let active = true;

        const fetchDashboard = async () => {
            try {
                const data = await getData("dashboard");
                
                if (active) {
                    setUser(data.user);
                }

            } catch (error) {
                console.error("Error fetching dashboard!");
            }
        };

        fetchDashboard();

        // Cleanup function
        return () => {
            active = false;
        };
        
    }, []);

    const handleLogout = async () => {
        try {
            await postData("logout", {});

            navigate("/login", { replace: true });
        } catch (error) {
            console.error("Logout failed:", error);
        }
    };

    const handleProfile = () => {
        navigate("/profile", { replace: true });
    }

    if (!user) {
        return (
            <div className="text-center mt-5">
                <div className="spinner-border text-primary" />
                <p>Loading dashboard...</p>
            </div>
        );
    }

    return (
        <div className="container mt-5">
            <nav className="navbar navbar-dark bg-primary rounded px-3">
                <div className="container-fluid">

                    <a className="navbar-brand fw-bold" href="/dashboard/">
                        AI Enquiry Assistant Demo
                    </a>

                    <div className="dropdown ms-auto">

                        <button
                            className="btn border-0 dropdown-toggle d-flex align-items-center"
                            type="button"
                            id="userDropdown"
                            data-bs-toggle="dropdown"
                            aria-expanded="false">

                            <img
                                src="https://i.pravatar.cc/40"
                                alt="User"
                                className="rounded-circle me-2"
                                width="40"
                                height="40" />

                            <span className="text-white">{user.last_name} {user.first_name}</span>
                        </button>

                        <ul className="dropdown-menu dropdown-menu-end"
                            aria-labelledby="userDropdown">

                            <li>
                                <a
                                    className="dropdown-item"
                                    type="button"
                                    onClick={handleProfile}
                                >
                                    <i className="bi bi-person me-2"></i>
                                    My Profile
                                </a>
                            </li>

                            <li><hr className="dropdown-divider" /></li>

                            <li>
                                <a
                                    className="dropdown-item"
                                    type="button"
                                    onClick={handleLogout}
                                >
                                    <i className="bi bi-lock me-2"></i>
                                    Logout
                                </a>
                            </li>

                        </ul>
                    </div>

                </div>
            </nav>

            <div className="card shadow border-0 mt-5">

                <div className="card-body p-5 text-center">

                    <h2>Welcome, {user.last_name}!</h2>

                    <p className="text-muted mt-3">
                        You are successfully authenticated.
                    </p>

                    <p>Email: {user.email}</p>

                    <span className="badge bg-success">
                        Authenticated
                    </span>
                    <ChatWidget />
                </div>

            </div>

            <div className="accordion accordion-flush" id="accordionFlushExample" style={{marginTop:"-10px"}}>
                <div className="accordion-item">
                    <h2 className="accordion-header">
                    <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                        About this Retrieval-Augmented Generation (RAG)
                    </button>
                    </h2>
                    <div id="flush-collapseOne" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                    <div className="accordion-body">
                        This AI Enquiry Assistant provides answers to questions related to academic offences. For example, you can ask: 
                        <b>"What are the consequences of an academic offence?"</b>, <b>"Does an academic offence appear on my transcript?"</b>, 
                        <b>"Who can access information about my academic offence?"</b>, or <b>"Can a former student be investigated?"</b> etc.
                    </div>
                    </div>
                </div>
                <div className="accordion-item">
                    <h2 className="accordion-header">
                    <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
                        Use Case
                    </button>
                    </h2>
                    <div id="flush-collapseTwo" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                    <div className="accordion-body">
                        <p>
                          Universities operate through numerous academic and administrative policies that guide students, lecturers, 
                          and non-academic staff in their daily activities. These policies cover critical areas such as admission 
                          requirements, course registration, graduation eligibility, examination regulations, deferment of admission, 
                          resit examinations, staff conduct, promotion procedures, and academic progression. However, despite the 
                          importance of these policies, access to clear and timely information remains a major challenge within many 
                          higher institutions.
                        </p>

                        <p>
                            Students often struggle to understand the requirements for graduation, conditions for course repetition, 
                            rules governing examination misconduct, procedures for deferment of studies, and other academic regulations.
                             In many cases, policy documents are scattered across multiple handbooks, websites, memos, and departmental 
                             publications, making it difficult for students to locate accurate and up-to-date information when needed. 
                             This lack of accessibility frequently leads to misinformation, missed deadlines, poor academic decisions, 
                             and unnecessary dependence on administrative offices for clarification.

                        </p>

                        <p>
                            Similarly, old and newly employed staff members face significant difficulties in familiarising themselves 
                            with the extensive policies and operational guidelines of the university. Staff may not fully understand 
                            institutional procedures relating to academic administration, staff responsibilities, promotion criteria, 
                            leave policies, or student management regulations. The inability to quickly retrieve relevant policy 
                            information can reduce efficiency, create inconsistencies in decision-making, and negatively affect service 
                            delivery within the institution.
                        </p>

                        <p>
                            The increasing volume and complexity of university regulations make traditional methods of information 
                            dissemination inadequate. Static documents and manual searches are often time-consuming, inefficient, and 
                            frustrating for users who require immediate answers to policy-related questions. Consequently, there is a growing 
                            need for an intelligent system capable of providing accurate, context-aware, and user-friendly access to university
                             policies and regulations.

                        </p>

                        <p>
                            To address this challenge, this help assistant combines the strengths of information retrieval and 
                            generative artificial intelligence to deliver precise and contextually relevant responses from a 
                            large collection of institutional documents. By integrating university policy documents into a centralised 
                            knowledge base, the system can retrieve the most relevant information and generate understandable responses 
                            to user queries in natural language.

                        </p>

                        <p>
                            The system enables students and staff to ask questions such as “What are the consequences of an academic 
                            offence?”, “Does an academic offence appear on my transcript?”, “Who can access information about my 
                            academic offence?”, or “Can a university investigate someone who has graduated?” and receive immediate, 
                            accurate, and policy-compliant answers. It reduces the workload on administrative offices by minimising 
                            repetitive inquiries, improve policy awareness across the university community, and promote consistency 
                            in the interpretation of institutional regulations.

                        </p>



                    </div>
                    </div>
                </div>
                
                </div>

        </div>
    );
}

export default Dashboard;
