/**
 * API Client - Axios instance with interceptors
 * Handles authentication, error handling, and base configuration
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { toast } from 'react-hot-toast';
import type { ApiError } from '@/types/api';

// Create axios instance with base configuration
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add Clerk auth token
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    // Get Clerk session token
    try {
      // Try to access Clerk from window
      if (typeof window !== 'undefined') {
        const clerk = (window as any).Clerk;

        // Check if Clerk is loaded and has a session
        if (clerk?.loaded && clerk?.session) {
          const token = await clerk.session.getToken();
          if (token) {
            config.headers.Authorization = `Bearer ${token}`;
          }
        }
      }
    } catch (error) {
      console.error('Error getting auth token:', error);
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors globally
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError<ApiError>) => {
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const message = error.response.data?.detail || 'An error occurred';

      switch (status) {
        case 400:
          toast.error(`Invalid request: ${message}`);
          break;
        case 401:
          toast.error('Please sign in to continue');
          break;
        case 403:
          toast.error('You do not have permission to perform this action');
          break;
        case 404:
          toast.error('Resource not found');
          break;
        case 422:
          toast.error(`Validation error: ${message}`);
          break;
        case 500:
          toast.error('Server error. Please try again later.');
          break;
        default:
          toast.error(message);
      }
    } else if (error.request) {
      // Request was made but no response received
      toast.error('Network error. Please check your connection.');
    } else {
      // Something else happened
      toast.error('An unexpected error occurred');
    }

    return Promise.reject(error);
  }
);

export default apiClient;
