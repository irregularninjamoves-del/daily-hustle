import { Heart, Trash2, ExternalLink } from 'lucide-react'
import { useState } from 'react'

export default function Saved() {
  const [activeTab, setActiveTab] = useState<'coupons' | 'hustles'>('coupons')
  
  // Mock saved items - in real app, fetch from API
  const savedCoupons: any[] = []
  const savedHustles: any[] = []

  return (
    <div className="p-4 space-y-4">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold flex items-center gap-2">
          <Heart className="h-5 w-5 text-red-500" />
          Saved Items
        </h1>
        <p className="text-gray-500 text-sm">Your bookmarked deals and opportunities</p>
      </div>
      
      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setActiveTab('coupons')}
          className={`flex-1 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'coupons'
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-500'
          }`}
        >
          Coupons ({savedCoupons.length})
        </button>
        <button
          onClick={() => setActiveTab('hustles')}
          className={`flex-1 py-3 text-sm font-medium border-b-2 transition-colors ${
            activeTab === 'hustles'
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-500'
          }`}
        >
          Hustles ({savedHustles.length})
        </button>
      </div>
      
      {/* Empty state */}
      <div className="text-center py-16">
        <div className="h-16 w-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Heart className="h-8 w-8 text-gray-400" />
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-1">
          No saved items yet
        </h3>
        <p className="text-gray-500 text-sm max-w-xs mx-auto">
          Browse deals and side hustles, then tap the heart icon to save them here for later.
        </p>
        <div className="flex gap-3 justify-center mt-6">
          <a
            href="/coupons"
            className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm font-medium hover:bg-primary-700 transition-colors"
          >
            Browse Deals
          </a>
          <a
            href="/hustles"
            className="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors"
          >
            Find Hustles
          </a>
        </div>
      </div>
    </div>
  )
}
