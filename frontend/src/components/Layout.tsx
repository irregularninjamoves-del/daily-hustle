import { Outlet, useLocation } from 'react-router-dom'
import { Home, Ticket, Briefcase, Bike, User, Sparkles } from 'lucide-react'

const navItems = [
  { path: '/', icon: Home, label: 'Home' },
  { path: '/recommendations', icon: Sparkles, label: 'For You' },
  { path: '/coupons', icon: Ticket, label: 'Deals' },
  { path: '/hustles', icon: Briefcase, label: 'Hustles' },
  { path: '/delivery', icon: Bike, label: 'Delivery' },
  { path: '/profile', icon: User, label: 'Profile' },
]

export default function Layout() {
  const location = useLocation()

  return (
    <div className="h-full flex flex-col">
      <main className="flex-1 overflow-y-auto pb-20">
        <Outlet />
      </main>
      
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 safe-bottom z-50">
        <div className="flex justify-around items-center h-16">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path
            const Icon = item.icon
            return (
              <a
                key={item.path}
                href={item.path}
                className={`flex flex-col items-center justify-center flex-1 h-full transition-colors ${
                  isActive ? 'text-primary-600' : 'text-gray-500'
                }`}
              >
                <Icon className="h-5 w-5" />
                <span className="text-xs mt-1">{item.label}</span>
              </a>
            )
          })}
        </div>
      </nav>
    </div>
  )
}
