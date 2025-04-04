import axios from 'axios';

// Determine the base URL for the API Gateway
// In development, this typically points to where the gateway is exposed (e.g., localhost:8000)
// In production, this would point to the deployed gateway URL.
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1'; 

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    // Add other default headers if needed, e.g., Authorization
  },
});

// Optional: Add interceptors for handling requests or responses globally
// For example, automatically adding an auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    // Retrieve token from storage (e.g., localStorage, Zustand store)
    const token = localStorage.getItem('authToken'); // Example: using localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Optional: Add interceptors for handling responses globally
// For example, handling 401 Unauthorized errors by redirecting to login
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // Handle unauthorized access, e.g., clear token, redirect to login
      console.error("Unauthorized access - redirecting to login.");
      localStorage.removeItem('authToken'); // Example cleanup
      // window.location.href = '/login'; // Example redirect
    }
    return Promise.reject(error);
  }
);


export default apiClient;
