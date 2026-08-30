import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000
})

api.interceptors.request.use((config) => {
  const storage = localStorage.getItem('auth-storage')
  const token = storage ? JSON.parse(storage).state?.token : null
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  login: (email: string, password: string) => api.post('/auth/login', { email, password }),
  register: (data: any) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
}

export const couponsAPI = {
  getAll: (params?: any) => api.get('/coupons/', { params }),
  getTrending: () => api.get('/coupons/trending'),
  save: (couponId: string) => api.post('/coupons/save', { coupon_id: couponId }),
}

export const hustlesAPI = {
  getAll: (params?: any) => api.get('/hustles/', { params }),
  getBikeFriendly: () => api.get('/hustles/bike-friendly'),
}

export const deliveryAPI = {
  getAll: (params?: any) => api.get('/delivery/', { params }),
  getBikeFriendly: () => api.get('/delivery/bike-friendly'),
}

export const recommendationsAPI = {
  getAll: (params?: any) => api.get('/recommendations/', { params }),
  getProfile: () => api.get('/recommendations/ml-profile'),
}

export const interactionsAPI = {
  log: (data: any) => api.post('/interactions/', data),
}

export const locationAPI = {
  update: (lat: number, lon: number) => api.post('/location/update', { lat, lon }),
  getNearby: (lat: number, lon: number, radius = 10) => 
    api.get(`/location/nearby-deals?lat=${lat}&lon=${lon}&radius_km=${radius}`),
}
