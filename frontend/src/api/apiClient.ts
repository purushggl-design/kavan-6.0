import axios from 'axios';
import { store } from '@/store';
import { setAccessToken, logout } from '@/store/authSlice';
import { ENDPOINTS } from './endpoints';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach JWT Token
apiClient.interceptors.request.use(
  (config) => {
    // Always get the freshest token from Redux state
    const state = store.getState();
    const token = state.auth.accessToken;
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401 & Token Refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const state = store.getState();
      const refreshToken = state.auth.refreshToken;
      
      if (!refreshToken) {
        store.dispatch(logout());
        return Promise.reject(error);
      }
      
      try {
        // Use a new axios instance to avoid infinite interceptor loops
        const refreshResponse = await axios.post(`${API_BASE_URL}${ENDPOINTS.AUTH.REFRESH}`, {
          refresh_token: refreshToken
        });
        
        const newAccessToken = refreshResponse.data?.data?.access_token;
        if (newAccessToken) {
          // Update Redux store with the new access token
          store.dispatch(setAccessToken(newAccessToken));
          
          // Update authorization header and retry original request
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return apiClient(originalRequest);
        } else {
          throw new Error('No token returned');
        }
      } catch (refreshError) {
        // Refresh failed (e.g. refresh token expired)
        store.dispatch(logout());
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
