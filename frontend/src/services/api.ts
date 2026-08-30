import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const authAPI = {
  login: (email: string, password: string) => 
    api.post('/auth/login', { email, password }),
  register: (data: { email: string; password: string; name?: string }) => 
    api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
}

export const couponsAPI = {
  getAll: (params?: Record<string, any>) => 
    api.get('/coupons/', { params }),
  getTrending: () => 
    api.get('/coupons/trending'),
  save: (couponId: string) => 
    api.post('/coupons/save', { coupon_id: couponId }),
}

export const hustlesAPI = {
  getAll: (params?: Record<string, any>) => 
    api.get('/hustles/', { params }),
  getBikeFriendly: () => 
    api.get('/hustles/bike-friendly'),
}

export const deliveryAPI = {
  getAll: (params?: Record<string, any>) => 
    api.get('/delivery/', { params }),
  getBikeFriendly: () => 
    api.get('/delivery/bike-friendly'),
}
