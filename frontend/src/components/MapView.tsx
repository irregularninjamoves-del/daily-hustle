import { useEffect, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

interface MapViewProps {
  center: [number, number]
  zoom?: number
  markers?: Array<{
    id: string
    lat: number
    lon: number
    title: string
    category?: string
  }>
  onMarkerClick?: (id: string) => void
}

export default function MapView({ center, zoom = 13, markers = [], onMarkerClick }: MapViewProps) {
  const mapRef = useRef<L.Map | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return
    
    // Initialize map
    mapRef.current = L.map(containerRef.current).setView(center, zoom)
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(mapRef.current)
    
    // Add user location marker
    L.marker(center).addTo(mapRef.current)
      .bindPopup('You are here')
      .openPopup()
    
    // Add deal markers
    markers.forEach(marker => {
      const color = marker.category === 'Food' ? 'red' : 
                   marker.category === 'Tech' ? 'blue' : 'green'
      
      const customIcon = L.divIcon({
        className: 'custom-marker',
        html: `<div style="background-color: ${color}; width: 24px; height: 24px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
        iconSize: [24, 24]
      })
      
      const m = L.marker([marker.lat, marker.lon], { icon: customIcon })
        .addTo(mapRef.current!)
        .bindPopup(marker.title)
      
      if (onMarkerClick) {
        m.on('click', () => onMarkerClick(marker.id))
      }
    })
    
    return () => {
      mapRef.current?.remove()
    }
  }, [center, zoom, markers])

  return (
    <div 
      ref={containerRef}
      className="w-full h-full min-h-[300px] rounded-xl"
      style={{ height: '100%' }}
    />
  )
}
