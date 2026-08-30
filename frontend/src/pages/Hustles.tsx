import { useEffect, useState } from 'react'
import { Search, Bike, ExternalLink, Clock, DollarSign } from 'lucide-react'
import { hustlesAPI } from '../services/api'

interface Hustle {
  id: string
  title: string
  company: string
  description: string
  hustle_type: string
  pay_rate: string
  is_bike_friendly: boolean
  is_remote: boolean
  apply_url: string
  rating: number
}

export default function Hustles() {
  const [hustles, setHustles] = useState<Hustle[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState<'all' | 'bike'>('all')
  
  useEffect(() => {
    const fetchHustles = async () => {
      try {
        const params = filter === 'bike' ? { is_bike_friendly: true } : {}
        const response = await hustlesAPI.getAll(params)
        setHustles(response.data.items || [])
      } catch (error) {
        console.error('Error fetching hustles:', error)
      } finally {
        setLoading(false)
      }
    }
    
    fetchHustles()
  }, [filter])
  
  const filteredHustles = hustles.filter(h => 
    h.title.toLowerCase().includes(search.toLowerCase()) ||
    h.company.toLowerCase().includes(search.toLowerCase())
  )
  
  if (loading) {
    return (
      <div className="p-4 space-y-4">
        <div className="h-10 bg-gray-200 rounded-lg animate-pulse"></div>
        {[1, 2, 3].map(i => (
          <div key={i} className="h-40 bg-gray-200 rounded-xl animate-pulse"></div>
        ))}
      </div>
    )
  }

  return (
    <div className="p-4 space-y-4">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold">Side Hustles</h1>
        <p className="text-gray-500 text-sm">Find ways to earn extra income</p>
      </div>
      
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search opportunities..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
        />
      </div>
      
      {/* Filter */}
      <div className="flex gap-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            filter === 'all' 
              ? 'bg-primary-600 text-white' 
              : 'bg-white text-gray-700 border border-gray-200'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setFilter('bike')}
          className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-1 transition-colors ${
            filter === 'bike' 
              ? 'bg-primary-600 text-white' 
              : 'bg-white text-gray-700 border border-gray-200'
          }`}
        >
          <Bike className="h-4 w-4" />
          Bike Friendly
        </button>
      </div>
      
      {/* Hustles list */}
      <div className="space-y-3">
        {filteredHustles.map((hustle) => (
          <div
            key={hustle.id}
            className="bg-white p-4 rounded-xl shadow-sm border border-gray-100"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-gray-900">{hustle.company}</span>
                  {hustle.is_bike_friendly && (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full flex items-center gap-1">
                      <Bike className="h-3 w-3" />
                      Bike
                    </span>
                  )}
                  {hustle.is_remote && (
                    <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
                      Remote
                    </span>
                  )}
                </div>
                <h3 className="text-gray-900 font-medium mb-1">{hustle.title}</h3>
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                  {hustle.description}
                </p>
                
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span className="flex items-center gap-1">
                    <DollarSign className="h-4 w-4 text-green-600" />
                    {hustle.pay_rate}
                  </span>
                  <span className="flex items-center gap-1">
                    {'★'.repeat(Math.round(hustle.rating))}
                    <span className="text-gray-400">({hustle.rating})</span>
                  </span>
                </div>
              </div>
            </div>
            
            <a
              href={hustle.apply_url}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-3 flex items-center justify-center gap-2 w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <span>Apply Now</span>
              <ExternalLink className="h-4 w-4" />
            </a>
          </div>
        ))}
        
        {filteredHustles.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <p>No opportunities found.</p>
          </div>
        )}
      </div>
    </div>
  )
}
