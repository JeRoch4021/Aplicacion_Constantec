import axios from 'axios'

const axiosClient = axios.create({
  baseURL: 'http://localhost:8000', // Replace with your API base URL
  headers: {
    'Content-Type': 'application/json',
    // Add other custom headers here
  },
  timeout: 10000,
})

// Optional: Add interceptors (for auth tokens, error handling, logging, etc.)
axiosClient.interceptors.request.use(
  (config) => {
    // Example: attach token
    // const token = localStorage.getItem("token");
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config
  },
  (error) => Promise.reject(error)
)

axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    return Promise.reject(error)
  }
)

export default axiosClient
