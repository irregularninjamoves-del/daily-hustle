import { useEffect, useState } from 'react'
import { Sparkles, TrendingUp } from 'lucide-react'
import { api } from '../services/api'

interface Recommendation {
  id: string
  type: 'coupon' | 'hustle'
  item: any
  total_score: number
  explanation: string
  is_exploration: boolean
}

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/recommendations/').then(r => {
      setRecommendations(r.data.items || [])
      setLoading(false)
    })
  }, [])

  const handleInteraction = async (id: string, type: string, action: string) => {
    await api.post('/interactions/', { item_type: type, item_id: id, action })
  }

  if (loading) return <div className="p-4 text-center">Loading...</div>

  return (
    <div className="p-4 space-y-4">
      <div className="bg-gradient-to-r from-purple-600 to-purple-700 text-white p-4 rounded-xl">
        <h1 className="font-bold text-lg flex items-center gap-2">
          <Sparkles className="h-5 w-5" />
          AI-Powered For You
        </h1>
        <p className="text-purple-100 text-sm">Personalized based on your interests</p>
      </div>

      {recommendations.map(rec => (
        <div key={rec.id} className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="font-semibold">
              {rec.type === 'coupon' ? rec.item.store_name : rec.item.company}
            </span>
            {rec.is_exploration && (
              <span className="text-xs bg-blue-100 text-blue-700 px-2 rounded-full">New</span>
            )}
          </div>
          <p className="text-gray-700">{rec.item.title}</p>
          <p className="text-xs text-gray-500 mt-1 italic">{rec.explanation}</p>
          <div className="flex gap-2 mt-3">
            <button onClick={() => handleInteraction(rec.id, rec.type, 'save')}
              className="flex-1 py-2 bg-primary-100 text-primary-700 rounded-lg text-sm">Save</button>
            <button onClick={() => handleInteraction(rec.id, rec.type, 'dismiss')}
              className="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg text-sm">✕</button>
          </div>
        </div>
      ))}

      {recommendations.length === 0 && (
        <div className="text-center py-12">
          <TrendingUp className="h-12 w-12 mx-auto mb-3 text-gray-300" />
          <p>Browse deals to get personalized recommendations!</p>
        </div>
      )}
    </div>
  )
}
