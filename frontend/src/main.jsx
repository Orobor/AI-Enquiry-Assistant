import React from 'react';
import ReactDOM from 'react-dom/client';

import './assets/bootstrap/bootstrap.min.css';
import './assets/bootstrap/bootstrap.bundle.min.js';

import App from './App';

ReactDOM.createRoot(
    document.getElementById('root')
).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);