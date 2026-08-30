import { useEffect, useState } from 'react'
import { Search, Copy, MapPin, ExternalLink, Filter } from 'lucide-react'
import { couponsAPI, interactionsAPI } from '../services/api'

interface Coupon {
  id: string
  store_name: string
  title: string
  description: string | null
  code: string | null
  discount_display: string
  category: string
  is_online_only: boolean
  store_lat?: number
  store_lon?: number
}

export default function Coupons() {
  const [coupons, setCoupons] = useState<Coupon[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const [showMap, setShowMap] = useState(false)
  const [location, setLocation] = useState<{lat: number, lon: number} | null>(null)
  const [category, setCategory] = useState<string>('')
  
  useEffect(() => {
    // Get location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setLocation({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
        () => console.log('Location denied')
      )
    }
    
    fetchCoupons()
  }, [])
  
  const fetchCoupons = async () => {
    try {
      const params: any = { limit: 50 }
      if (category) params.category = category
      if (location) {
        params.lat = location.lat
        params.lon = location.lon
        params.radius_km = 10
      }
      
      const response = await couponsAPI.getAll(params)
      setCoupons(response.data.items || [])
    } catch (error) {
      console.error('Error fetching coupons:', error)
    } finally {
      setLoading(false)
    }
  }
  
  const handleCopyCode = async (code: string | null, id: string) => {
    if (code) {
      navigator.clipboard.writeText(code)
      setCopiedId(id)
      setTimeout(() => setCopiedId(null), 2000)
      
      // Log interaction
      await interactionsAPI.log({ item_type: 'coupon', item_id: id, action: 'copy' })
    }
  }
  
  const handleSave = async (id: string) => {
    try {
      await couponsAPI.save(id)
      await interactionsAPI.log({ item_type: 'coupon', item_id: id, action: 'save' })
      alert('Coupon saved!')
    } catch (error) {
      console.error('Error saving:', error)
    }
  }
  
  const filteredCoupons = coupons.filter(c => 
    c.store_name.toLowerCase().includes(search.toLowerCase()) ||
    c.title.toLowerCase().includes(search.toLowerCase())
  )
  
  const categories = ['Food', 'Tech', 'Fashion', 'Home', 'Health']
  
  if (loading) {
    return (
      <div className="p-4 space-y-4">
        <div className="h-10 bg-gray-200 rounded-lg animate-pulse"></div>
        {[1, 2, 3].map(i => (
          <div key={i} className="h-32 bg-gray-200 rounded-xl animate-pulse"></div>
        ))}
      </div>
    )
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center gap-3">
        <h1 className="text-xl font-bold">Deals & Coupons</h1>
        {location && (
          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
            Nearby
          </span>
        )}
      </div>
      
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search stores or deals..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>
      
      <div className="flex gap-2 overflow-x-auto pb-2">
        <button
          onClick={() => setCategory('')}
          className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap ${
            category === '' ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700'
          }`}
        >
          All
        </button>
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setCategory(cat)}
            className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap ${
              category === cat ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-700'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>
      
      <div className="space-y-3">
        {filteredCoupons.map((coupon) => (
          <div
            key={coupon.id}
            className="bg-white p-4 rounded-xl shadow-sm border border-gray-100"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-gray-900">{coupon.store_name}</span>
                  {coupon.is_online_only && (
                    <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">Online</span>
                  )}
                  {coupon.store_lat && (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full flex items-center gap-1">
                      <MapPin className="h-3 w-3" />
                      Nearby
                    </span>
                  )}
                </div>
                <p className="text-gray-700 text-sm mb-2">{coupon.title}</p>
                <span className="bg-gray-100 px-2 py-1 rounded text-xs text-gray-600">
                  {coupon.category}
                </span>
              </div>
              
              <div className="text-right">
                <p className="text-lg font-bold text-primary-600">{coupon.discount_display}</p>
              </div>
            </div>
            
            {coupon.code && (
              <div className="mt-3 flex items-center gap-2">
                <button
                  onClick={() => handleCopyCode(coupon.code, coupon.id)}
                  className="flex-1 flex items-center justify-center gap-2 bg-gray-100 hover:bg-gray-200 py-2 px-4 rounded-lg transition-colors"
                >
                  <Copy className="h-4 w-4" />
                  <span className="font-mono text-sm">
                    {copiedId === coupon.id ? 'Copied!' : coupon.code}
                  </span>
                </button>
                <button
                  onClick={() => handleSave(coupon.id)}
                  className="p-2 bg-primary-100 text-primary-600 rounded-lg hover:bg-primary-200"
                >
                  <ExternalLink className="h-4 w-4" />
                </button>
              </div>
            )}
          </div>
        ))}
        
        {filteredCoupons.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <p>No coupons found.</p>
          </div>
        )}
      </div>
    </div>
  )
}
