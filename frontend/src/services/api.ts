import axios from 'axios';

// Base URL: use env var in production, or relative path (Vite proxy) in development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle 401s and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) throw new Error('No refresh token available');
        
        // Call refresh endpoint directly using axios to avoid loops
        const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh_token: refreshToken
        });
        
        if (response.data?.data?.access_token) {
          localStorage.setItem('access_token', response.data.data.access_token);
          if (response.data.data.refresh_token) {
             localStorage.setItem('refresh_token', response.data.data.refresh_token);
          }
          // Update authorization header and retry original request
          originalRequest.headers.Authorization = `Bearer ${response.data.data.access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // If refresh fails, clear tokens and let the UI redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.dispatchEvent(new Event('auth:unauthorized'));
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
