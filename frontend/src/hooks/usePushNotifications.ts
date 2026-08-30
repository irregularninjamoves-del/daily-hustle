import { useState, useEffect } from 'react'
import { api } from '../services/api'

const PUBLIC_VAPID_KEY = 'YOUR_VAPID_PUBLIC_KEY' // Replace with actual key

export function usePushNotifications() {
  const [isSupported, setIsSupported] = useState(false)
  const [subscription, setSubscription] = useState<PushSubscription | null>(null)
  const [permission, setPermission] = useState<NotificationPermission>('default')

  useEffect(() => {
    if ('Notification' in window && 'serviceWorker' in navigator && 'PushManager' in window) {
      setIsSupported(true)
      setPermission(Notification.permission)
      checkSubscription()
    }
  }, [])

  const checkSubscription = async () => {
    try {
      const registration = await navigator.serviceWorker.ready
      const sub = await registration.pushManager.getSubscription()
      setSubscription(sub)
    } catch (error) {
      console.error('Error checking subscription:', error)
    }
  }

  const urlBase64ToUint8Array = (base64String: string): Uint8Array => {
    const padding = '='.repeat((4 - base64String.length % 4) % 4)
    const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/')
    const rawData = window.atob(base64)
    return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)))
  }

  const subscribe = async (): Promise<boolean> => {
    if (!isSupported) return false

    try {
      // Request permission
      const permissionResult = await Notification.requestPermission()
      setPermission(permissionResult)

      if (permissionResult !== 'granted') {
        return false
      }

      // Subscribe
      const registration = await navigator.serviceWorker.ready
      const sub = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(PUBLIC_VAPID_KEY)
      })

      setSubscription(sub)

      // Send to server
      await api.post('/notifications/subscribe', sub.toJSON())

      return true
    } catch (error) {
      console.error('Error subscribing:', error)
      return false
    }
  }

  const unsubscribe = async (): Promise<void> => {
    try {
      if (subscription) {
        await subscription.unsubscribe()
        await api.post('/notifications/unsubscribe')
        setSubscription(null)
      }
    } catch (error) {
      console.error('Error unsubscribing:', error)
    }
  }

  const sendTestNotification = async (): Promise<void> => {
    await api.post('/notifications/test')
  }

  return {
    isSupported,
    isSubscribed: !!subscription,
    permission,
    subscribe,
    unsubscribe,
    sendTestNotification
  }
}
