"""Push notification service using Web Push"""
import json
import logging
from typing import Optional
from pywebpush import webpush, WebPushException

from ..config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# VAPID keys should be configured in environment
VAPID_PRIVATE_KEY = getattr(settings, 'VAPID_PRIVATE_KEY', None)
VAPID_CLAIMS = {
    "sub": "mailto:admin@dailyhustle.app"
}


class PushSubscription:
    """Represents a push subscription from a client"""
    def __init__(self, endpoint: str, p256dh: str, auth: str):
        self.endpoint = endpoint
        self.p256dh = p256dh
        self.auth = auth
    
    def to_dict(self):
        return {
            "endpoint": self.endpoint,
            "keys": {
                "p256dh": self.p256dh,
                "auth": self.auth
            }
        }


async def send_push_notification(
    subscription: dict,
    title: str,
    body: str,
    icon: str = "/icon-192.png",
    badge: str = "/icon-72.png",
    data: dict = None
):
    """Send a push notification to a subscriber"""
    
    if not VAPID_PRIVATE_KEY:
        logger.warning("VAPID_PRIVATE_KEY not configured, skipping push")
        return False
    
    try:
        notification_payload = {
            "notification": {
                "title": title,
                "body": body,
                "icon": icon,
                "badge": badge,
                "tag": "daily-hustle-alert",
                "requireInteraction": True,
                "data": data or {}
            }
        }
        
        webpush(
            subscription_info=subscription,
            data=json.dumps(notification_payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        
        logger.info(f"Push notification sent: {title}")
        return True
        
    except WebPushException as e:
        logger.error(f"Push notification failed: {e}")
        return False


async def send_geofence_alert(
    subscription: dict,
    store_name: str,
    deal_title: str,
    coupon_id: str
):
    """Send geofence alert notification"""
    return await send_push_notification(
        subscription=subscription,
        title=f"📍 You're near {store_name}!",
        body=f"{deal_title} - Tap to view and save",
        data={
            "type": "geofence",
            "coupon_id": coupon_id,
            "store_name": store_name
        }
    )


async def send_daily_digest(
    subscription: dict,
    deal_count: int
):
    """Send daily deals digest"""
    return await send_push_notification(
        subscription=subscription,
        title="🔥 Your Daily Hustle Digest",
        body=f"{deal_count} new deals matched your interests today",
        data={"type": "digest", "screen": "/"}
    )
