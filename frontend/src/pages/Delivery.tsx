import { useEffect, useState } from 'react'
import { Bike, ExternalLink, Check, X } from 'lucide-react'
import { deliveryAPI } from '../services/api'

interface DeliveryService {
  id: string
  company_name: string
  accepts_bikes: boolean
  accepts_walking: boolean
  min_age: number
  background_check_required: boolean
  pay_estimate_hourly: string
  signup_bonus: string | null
  signup_url: string
  overall_rating: number
  pros: string[]
  cons: string[]
}

export default function Delivery() {
  const [services, setServices] = useState<DeliveryService[]>([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await deliveryAPI.getBikeFriendly()
        setServices(response.data.items || [])
      } catch (error) {
        console.error('Error:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchServices()
  }, [])
  
  if (loading) {
    return (
      <div className="p-4 space-y-4">
        <div className="h-20 bg-gray-200 rounded-xl animate-pulse"></div>
        {[1, 2, 3].map(i => (
          <div key={i} className="h-48 bg-gray-200 rounded-xl animate-pulse"></div>
        ))}
      </div>
    )
  }

  return (
    <div className="p-4 space-y-4">
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-4 rounded-xl">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <Bike className="h-6 w-6" />
          Bike Delivery
        </h1>
        <p className="text-primary-100 text-sm mt-1">Earn money delivering by bike!</p>
      </div>
      
      <div className="space-y-4">
        {services.map((service) => (
          <div key={service.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="p-4 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-lg">{service.company_name}</h3>
                <div className="flex items-center gap-1 text-yellow-500">
                  <span className="font-bold">{service.overall_rating}</span>
                  <span className="text-sm">★</span>
                </div>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                {service.accepts_bikes && (
                  <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full flex items-center gap-1">
                    <Bike className="h-3 w-3" />
                    Bike OK
                  </span>
                )}
                {service.background_check_required && (
                  <span className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full">Background Check</span>
                )}
              </div>
            </div>
            
            <div className="p-4 space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Pay</p>
                  <p className="font-semibold text-green-600">{service.pay_estimate_hourly}/hr</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Min Age</p>
                  <p className="font-semibold">{service.min_age}+</p>
                </div>
              </div>
              
              {service.signup_bonus && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                  <p className="text-sm font-medium text-yellow-800">🎁 Bonus: {service.signup_bonus}</p>
                </div>
              )}
              
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="font-medium text-gray-700 mb-1">Pros</p>
                  <ul className="space-y-1">
                    {service.pros.slice(0, 2).map((pro, i) => (
                      <li key={i} className="flex items-center gap-1 text-green-600">
                        <Check className="h-3 w-3" />
                        <span className="text-gray-600">{pro}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="font-medium text-gray-700 mb-1">Cons</p>
                  <ul className="space-y-1">
                    {service.cons.slice(0, 2).map((con, i) => (
                      <li key={i} className="flex items-center gap-1 text-red-500">
                        <X className="h-3 w-3" />
                        <span className="text-gray-600">{con}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <a
                href={service.signup_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
              >
                <span>Sign Up</span>
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
          </div>
        ))}
        
        {services.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <Bike className="h-12 w-12 mx-auto mb-3 text-gray-300" />
            <p>No bike delivery services available.</p>
          </div>
        )}
      </div>
    </div>
  )
}
