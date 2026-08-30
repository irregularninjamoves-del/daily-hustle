import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Mock data for demo mode
const mockData = {
  coupons: [
    { id: '1', store_name: 'Target', title: '20% off home items', discount_display: '20% off', category: 'Home', code: 'HOME20', is_online_only: true },
    { id: '2', store_name: 'Walgreens', title: '$5 off $25+', discount_display: '$5 off', category: 'Health', code: 'GET5', is_online_only: false },
    { id: '3', store_name: 'Pizza Hut', title: 'BOGO Free Pizza', discount_display: 'BOGO', category: 'Food', code: null, is_online_only: false },
    { id: '4', store_name: 'Nike', title: 'Free shipping', discount_display: 'Free Shipping', category: 'Fashion', code: null, is_online_only: true },
    { id: '5', store_name: 'Amazon', title: '40% off electronics', discount_display: '40% off', category: 'Tech', code: null, is_online_only: true },
    { id: '6', store_name: 'Starbucks', title: '$2 off grande', discount_display: '$2 off', category: 'Food', code: 'COFFEE2', is_online_only: false },
    { id: '7', store_name: 'Best Buy', title: '$50 off laptops', discount_display: '$50 off', category: 'Tech', code: 'LAPTOP50', is_online_only: true },
    { id: '8', store_name: 'DoorDash', title: '50% off first order', discount_display: '50% off', category: 'Food', code: 'YUMMY50', is_online_only: true },
  ],
  hustles: [
    { id: '1', company: 'DoorDash', title: 'Deliver with DoorDash', description: 'Make money delivering food', pay_rate: '$15-25/hr', is_bike_friendly: true, is_remote: false, rating: 4.2 },
    { id: '2', company: 'Uber', title: 'Uber Eats Delivery', description: 'Deliver food on your schedule', pay_rate: '$12-22/hr', is_bike_friendly: true, is_remote: false, rating: 4.0 },
    { id: '3', company: 'Upwork', title: 'Freelance on Upwork', description: 'Find freelance work', pay_rate: '$10-100+/hr', is_bike_friendly: false, is_remote: true, rating: 4.3 },
    { id: '4', company: 'Prolific', title: 'Paid Surveys', description: 'Participate in research', pay_rate: '$6-15/hr', is_bike_friendly: false, is_remote: true, rating: 4.5 },
  ],
  delivery: [
    { id: '1', company_name: 'DoorDash', accepts_bikes: true, pay_estimate_hourly: '$15-25', overall_rating: 4.2, pros: ['Flexible', 'Bike mode'], cons: ['Wear on bike'] },
    { id: '2', company_name: 'Uber Eats', accepts_bikes: true, pay_estimate_hourly: '$12-22', overall_rating: 4.0, pros: ['Instant Pay', 'Walking mode'], cons: ['Expenses'] },
    { id: '3', company_name: 'Grubhub', accepts_bikes: true, pay_estimate_hourly: '$13-18', overall_rating: 3.9, pros: ['Scheduled blocks'], cons: ['Limited bike zones'] },
  ]
}

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: { 'Content-Type': 'application/json' },
  timeout: 5000
})

const isDemoMode = true

export const couponsAPI = {
  getAll: async (params?: Record<string, any>) => {
    if (isDemoMode) {
      return { data: { items: mockData.coupons, total: mockData.coupons.length } }
    }
    return api.get('/coupons/', { params })
  },
  getTrending: async () => {
    if (isDemoMode) {
      return { data: { items: mockData.coupons.slice(0, 4) } }
    }
    return api.get('/coupons/trending')
  },
  save: async (couponId: string) => {
    if (isDemoMode) return { data: { success: true } }
    return api.post('/coupons/save', { coupon_id: couponId })
  }
}

export const hustlesAPI = {
  getAll: async (params?: Record<string, any>) => {
    if (isDemoMode) {
      let items = mockData.hustles
      if (params?.is_bike_friendly) {
        items = items.filter(h => h.is_bike_friendly)
      }
      return { data: { items, total: items.length } }
    }
    return api.get('/hustles/', { params })
  },
  getBikeFriendly: async () => {
    if (isDemoMode) {
      return { data: { items: mockData.hustles.filter(h => h.is_bike_friendly) } }
    }
    return api.get('/hustles/bike-friendly')
  }
}

export const deliveryAPI = {
  getAll: async (params?: Record<string, any>) => {
    if (isDemoMode) {
      return { data: { items: mockData.delivery } }
    }
    return api.get('/delivery/', { params })
  },
  getBikeFriendly: async () => {
    if (isDemoMode) {
      return { data: { items: mockData.delivery.filter(d => d.accepts_bikes) } }
    }
    return api.get('/delivery/bike-friendly')
  }
}

export const authAPI = {
  login: async (email: string, password: string) => {
    return { data: { access_token: 'demo-token' } }
  },
  register: async (data: any) => {
    return { data: { access_token: 'demo-token' } }
  },
  me: async () => {
    return { data: { id: 'demo', email: 'you@dailyhustle.app', name: 'You' } }
  }
}
