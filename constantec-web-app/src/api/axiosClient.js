import axios from 'axios'

const axiosClient = axios.create({
  baseURL: '/', // Replace with your API base URL
  headers: {
    'Content-Type': 'application/json',
    // Add other custom headers here
  },
  timeout: 10000,
})

// Optional: Add interceptors (for auth tokens, error handling, logging, etc.)
axiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
)

axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado, redirigir al login
      alert("Su sessión ha expirado por inactividad.");
      localStorage.clear();
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
)

export default axiosClient
