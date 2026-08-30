import { useEffect, useState } from 'react'
import { MapPin, TrendingUp, DollarSign, Zap } from 'lucide-react'
import { couponsAPI, hustlesAPI, deliveryAPI } from '../services/api'

export default function Dashboard() {
  const [stats, setStats] = useState({ coupons: 0, hustles: 0, delivery: 0 })
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [couponsRes, hustlesRes, deliveryRes] = await Promise.all([
          couponsAPI.getTrending(),
          hustlesAPI.getBikeFriendly(),
          deliveryAPI.getBikeFriendly()
        ])
        
        setStats({
          coupons: couponsRes.data.items?.length || 0,
          hustles: hustlesRes.data.items?.length || 0,
          delivery: deliveryRes.data.items?.length || 0
        })
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [])
  
  if (loading) {
    return (
      <div className="p-4 space-y-4">
        <div className="h-8 bg-gray-200 rounded animate-pulse"></div>
        <div className="grid grid-cols-2 gap-4">
          <div className="h-24 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-24 bg-gray-200 rounded animate-pulse"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Daily Hustle</h1>
          <p className="text-gray-500 text-sm flex items-center gap-1">
            <MapPin className="h-4 w-4" />
            <span>Your personalized deals</span>
          </p>
        </div>
        <div className="h-10 w-10 bg-primary-100 rounded-full flex items-center justify-center">
          <Zap className="h-5 w-5 text-primary-600" />
        </div>
      </div>
      
      {/* Stats */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 text-primary-600 mb-2">
            <TrendingUp className="h-5 w-5" />
            <span className="font-medium">Active Deals</span>
          </div>
          <p className="text-3xl font-bold">{stats.coupons}</p>
          <p className="text-sm text-gray-500">Coupons available</p>
        </div>
        
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 text-green-600 mb-2">
            <DollarSign className="h-5 w-5" />
            <span className="font-medium">Opportunities</span>
          </div>
          <p className="text-3xl font-bold">{stats.hustles + stats.delivery}</p>
          <p className="text-sm text-gray-500">Side hustles & delivery</p>
        </div>
      </div>
      
      {/* Quick actions */}
      <div className="space-y-3">
        <h2 className="font-semibold text-gray-900">Quick Actions</h2>
        
        <a
          href="/coupons"
          className="block bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:border-primary-300 transition-colors"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 bg-orange-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="h-5 w-5 text-orange-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Browse Deals</p>
                <p className="text-sm text-gray-500">Find coupons near you</p>
              </div>
            </div>
            <span className="text-primary-600">→</span>
          </div>
        </a>
        
        <a
          href="/delivery"
          className="block bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:border-primary-300 transition-colors"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 bg-green-100 rounded-lg flex items-center justify-center">
                <DollarSign className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Start Earning</p>
                <p className="text-sm text-gray-500">Bike delivery opportunities</p>
              </div>
            </div>
            <span className="text-primary-600">→</span>
          </div>
        </a>
      </div>
    </div>
  )
}
