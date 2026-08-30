import { useEffect, useState } from 'react'
import { Search, Copy, MapPin, ExternalLink } from 'lucide-react'
import { couponsAPI } from '../services/api'

interface Coupon {
  id: string
  store_name: string
  title: string
  description: string | null
  code: string | null
  discount_display: string
  category: string
  is_online_only: boolean
}

export default function Coupons() {
  const [coupons, setCoupons] = useState<Coupon[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [copiedId, setCopiedId] = useState<string | null>(null)
  
  useEffect(() => {
    const fetchCoupons = async () => {
      try {
        const response = await couponsAPI.getAll({ limit: 20 })
        setCoupons(response.data.items || [])
      } catch (error) {
        console.error('Error fetching coupons:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchCoupons()
  }, [])
  
  const handleCopyCode = (code: string | null, id: string) => {
    if (code) {
      navigator.clipboard.writeText(code)
      setCopiedId(id)
      setTimeout(() => setCopiedId(null), 2000)
    }
  }
  
  const filteredCoupons = coupons.filter(c => 
    c.store_name.toLowerCase().includes(search.toLowerCase()) ||
    c.title.toLowerCase().includes(search.toLowerCase()) ||
    c.category.toLowerCase().includes(search.toLowerCase())
  )
  
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
      {/* Header */}
      <div className="flex items-center gap-3">
        <h1 className="text-xl font-bold">Deals & Coupons</h1>
      </div>
      
      {/* Search */}
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
      
      {/* Coupons list */}
      <div className="space-y-3">
        {filteredCoupons.map((coupon) => (
          <div
            key={coupon.id}
            className="bg-white p-4 rounded-xl shadow-sm border border-gray-100"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-gray-900">
                    {coupon.store_name}
                  </span>
                  {coupon.is_online_only && (
                    <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
                      Online
                    </span>
                  )}
                </div>
                <p className="text-gray-700 text-sm mb-2">{coupon.title}</p>
                <div className="flex items-center gap-2 text-xs text-gray-500">
                  <span className="bg-gray-100 px-2 py-1 rounded">
                    {coupon.category}
                  </span>
                </div>
              </div>
              
              <div className="text-right">
                <p className="text-lg font-bold text-primary-600">
                  {coupon.discount_display}
                </p>
              </div>
            </div>
            
            {/* Code section */}
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
                <a
                  href={coupon.id}
                  className="p-2 bg-primary-100 text-primary-600 rounded-lg hover:bg-primary-200 transition-colors"
                >
                  <ExternalLink className="h-4 w-4" />
                </a>
              </div>
            )}
          </div>
        ))}
        
        {filteredCoupons.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <p>No coupons found matching your search.</p>
          </div>
        )}
      </div>
    </div>
  )
}
