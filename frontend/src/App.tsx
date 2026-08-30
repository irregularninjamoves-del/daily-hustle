import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Coupons from './pages/Coupons'
import Hustles from './pages/Hustles'
import Delivery from './pages/Delivery'
import Saved from './pages/Saved'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Recommendations from './pages/Recommendations'
import { useAuthStore } from './stores/authStore'

function App() {
  const { initialize } = useAuthStore()
  
  useEffect(() => {
    initialize()
  }, [])

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="coupons" element={<Coupons />} />
          <Route path="hustles" element={<Hustles />} />
          <Route path="delivery" element={<Delivery />} />
          <Route path="saved" element={<Saved />} />
          <Route path="profile" element={<Profile />} />
          <Route path="recommendations" element={<Recommendations />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
