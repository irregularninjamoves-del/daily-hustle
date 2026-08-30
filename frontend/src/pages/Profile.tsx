import { useState } from 'react'
import { User, Bike, MapPin, LogOut, Bell, Shield, ChevronRight } from 'lucide-react'
import { useAuthStore } from '../stores/authStore'

export default function Profile() {
  const { user, logout } = useAuthStore()
  const [hasBike, setHasBike] = useState(true)
  const [notifications, setNotifications] = useState(true)
  
  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  return (
    <div className="p-4 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center">
          <User className="h-8 w-8 text-primary-600" />
        </div>
        <div>
          <h1 className="font-bold text-lg">{user?.name || user?.email || 'User'}</h1>
          <p className="text-gray-500 text-sm">{user?.email}</p>
        </div>
      </div>
      
      {/* Stats */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-white p-3 rounded-xl text-center border border-gray-100">
          <p className="text-2xl font-bold text-primary-600">12</p>
          <p className="text-xs text-gray-500">Deals Used</p>
        </div>
        <div className="bg-white p-3 rounded-xl text-center border border-gray-100">
          <p className="text-2xl font-bold text-green-600">$45</p>
          <p className="text-xs text-gray-500">Saved</p>
        </div>
        <div className="bg-white p-3 rounded-xl text-center border border-gray-100">
          <p className="text-2xl font-bold text-blue-600">3</p>
          <p className="text-xs text-gray-500">Active</p>
        </div>
      </div>
      
      {/* Settings */}
      <div className="space-y-4">
        <h2 className="font-semibold text-gray-900">Preferences</h2>
        
        <div className="bg-white rounded-xl border border-gray-100 overflow-hidden">
          <label className="flex items-center justify-between p-4 border-b border-gray-100">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 bg-green-100 rounded-lg flex items-center justify-center">
                <Bike className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">I have a bike</p>
                <p className="text-sm text-gray-500">Show bike-friendly options</p>
              </div>
            </div>
            <input
              type="checkbox"
              checked={hasBike}
              onChange={(e) => setHasBike(e.target.checked)}
              className="h-5 w-5 text-primary-600 rounded"
            />
          </label>
          
          <label className="flex items-center justify-between p-4">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Bell className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Notifications</p>
                <p className="text-sm text-gray-500">Deal alerts nearby</p>
              </div>
            </div>
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
              className="h-5 w-5 text-primary-600 rounded"
            />
          </label>
        </div>
      </div>
      
      {/* Location */}
      <div className="bg-white rounded-xl border border-gray-100 p-4">
        <div className="flex items-center gap-3 mb-3">
          <div className="h-10 w-10 bg-orange-100 rounded-lg flex items-center justify-center">
            <MapPin className="h-5 w-5 text-orange-600" />
          </div>
          <div>
            <p className="font-medium text-gray-900">Your Location</p>
            <p className="text-sm text-gray-500">Used for nearby deals</p>
          </div>
        </div>
        <button className="w-full py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
          Update Location
        </button>
      </div>
      
      {/* ML Status */}
      <div className="bg-gradient-to-r from-primary-50 to-primary-100 rounded-xl p-4">
        <div className="flex items-center gap-3 mb-2">
          <div className="h-10 w-10 bg-primary-200 rounded-lg flex items-center justify-center">
            <Shield className="h-5 w-5 text-primary-700" />
          </div>
          <div>
            <p className="font-medium text-primary-900">AI Recommendations</p>
            <p className="text-sm text-primary-700">Learning your preferences...</p>
          </div>
        </div>
        <div className="w-full bg-primary-200 rounded-full h-2 mt-3">
          <div className="bg-primary-600 h-2 rounded-full" style={{ width: '65%' }}></div>
        </div>
        <p className="text-xs text-primary-700 mt-2">
          Interact with more deals to improve recommendations!
        </p>
      </div>
      
      {/* Logout */}
      <button
        onClick={handleLogout}
        className="w-full flex items-center justify-center gap-2 py-3 bg-red-50 text-red-600 rounded-xl font-medium hover:bg-red-100 transition-colors"
      >
        <LogOut className="h-5 w-5" />
        Sign Out
      </button>
    </div>
  )
}
