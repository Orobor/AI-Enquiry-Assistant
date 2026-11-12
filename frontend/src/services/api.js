// Usage

// GET
// const users = await getData("users");

// POST
// const newUser = await postData("users", {
//     first_name: "Ise",
//     last_name: "Orobor",
//     email: "orobor.ise@gmail.com",
//     password: "securepassword",
// });

// PUT
// const updatedUser = await putData("users/1", {
//     first_name: "Ise",
//     last_name: "Orobor",
// });

// PATCH
// const patchedUser = await patchData("users/1", {
//     first_name: "Ise",
//     last_name: "Orobor",
// });

// DELETE
// await deleteData("users/1");

//

const API_URL = "http://localhost:8000/api";

// CSRF token
export async function generateCsrfToken() {
    
    const response = await fetch(`${API_URL}/csrf/`, {
        credentials: "include",
    });
    
    //console.log("CSRF response:", response);
    
    const data = await response.json();
    
    if (!response.ok) {
        
        // Extract Django REST Framework validation errors.
        const errorMessage = Object.values(data)
            .flat()
            .join(" ");

        throw new Error(errorMessage || "Request failed");

    }

    return data.csrfToken;
}


// GET request
export async function getData(endpoint) {
    const response = await fetch(`${API_URL}/${endpoint}/`, {
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
        },
    });

    const data = await response.json();

    if (!response.ok) {
        
        // Extract Django REST Framework validation errors.
        const errorMessage = Object.values(data)
            .flat()
            .join(" ");

        throw new Error(errorMessage || "Request failed");

    }

    return data
}


// POST request
export async function postData(endpoint, body) {

    const csrfToken = await generateCsrfToken();
    
    const response = await fetch(`${API_URL}/${endpoint}/`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
        
        // Extract Django REST Framework validation errors.
        const errorMessage = Object.values(data)
            .flat()
            .join(" ");

        throw new Error(errorMessage || "Request failed");

    }

    return data
}


// PUT request (update entire resource)
export async function putData(endpoint, body) {
    const csrfToken = await generateCsrfToken();

    const response = await fetch(`${API_URL}/${endpoint}/`, {
        method: "PUT",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
        
        // Extract Django REST Framework validation errors.
        const errorMessage = Object.values(data)
            .flat()
            .join(" ");

        throw new Error(errorMessage || "Request failed");

    }

    return data
}


// PATCH request (partial update)
export async function patchData(endpoint, body) {
    const csrfToken = await generateCsrfToken();

    const response = await fetch(`${API_URL}/${endpoint}/`, {
        method: "PATCH",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
        
        // Extract Django REST Framework validation errors.
        const errorMessage = Object.values(data)
            .flat()
            .join(" ");

        throw new Error(errorMessage || "Request failed");

    }

    return data
}


// DELETE request
export async function deleteData(endpoint) {
    const csrfToken = await generateCsrfToken();

    const response = await fetch(`${API_URL}/${endpoint}/`, {
        method: "DELETE",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
    });

    const data = await response.json();

    if (!response.ok) {
        
        // Extract Django REST Framework validation errors.
        const errorMessage = Object.values(data)
            .flat()
            .join(" ");

        throw new Error(errorMessage || "Request failed");

    }

    // Some DELETE endpoints return no content (204)
    if (response.status === 204) {
        return null;
    }

        return data

}

