import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  name: string
}

interface AuthState {
  token: string | null
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  setToken: (token: string) => void
  setUser: (user: User) => void
  logout: () => void
  initialize: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: true,
      
      setToken: (token) => set({ token, isAuthenticated: true }),
      
      setUser: (user) => set({ user }),
      
      logout: () => set({ token: null, user: null, isAuthenticated: false }),
      
      initialize: () => set({ isLoading: false })
    }),
    {
      name: 'auth-storage',
    }
  )
)
