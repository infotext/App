```python
import firebase_admin
from firebase_admin import credentials, messaging
import streamlit as st
import json

class PrayerNotifications:
    def __init__(self):
        # Firebase setup
        if not firebase_admin._apps:
            cred = credentials.Certificate({
                "type": st.secrets["FIREBASE_TYPE"],
                "project_id": st.secrets["FIREBASE_PROJECT_ID"],
                "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
                "private_key": st.secrets["FIREBASE_PRIVATE_KEY"],
                "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
                "client_id": st.secrets["FIREBASE_CLIENT_ID"],
                "auth_uri": st.secrets["FIREBASE_AUTH_URI"],
                "token_uri": st.secrets["FIREBASE_TOKEN_URI"],
                "auth_provider_x509_cert_url": st.secrets["FIREBASE_AUTH_CERT_URL"],
                "client_x509_cert_url": st.secrets["FIREBASE_CLIENT_CERT_URL"]
            })
            firebase_admin.initialize_app(cred)
    
    def send_prayer_notification(self, user_token, prayer_data):
        """Send push notification for prayer requests"""
        message = messaging.Message(
            notification=messaging.Notification(
                title="🙏 New Prayer Request",
                body=f"{prayer_data['user_name']} needs your prayers: {prayer_data['prayer_type']}",
                image="https://your-app.com/prayer-icon.png"
            ),
            data={
                'prayer_id': str(prayer_data['prayer_id']),
                'type': 'NEW_PRAYER',
                'urgency': prayer_data.get('urgency', 'medium'),
                'timestamp': prayer_data['timestamp']
            },
            token=user_token,
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    icon='prayer_notification',
                    color='#FF4B4B',
                    sound='default',
                    tag='prayer_request'
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(
                            title="Prayer Alert",
                            body="Someone needs your prayers",
                            launch_image="prayer_icon.png"
                        ),
                        sound='default',
                        badge=1,
                        category='PRAYER_CATEGORY'
                    )
                )
            )
        )
        
        try:
            response = messaging.send(message)
            return {'success': True, 'message_id': response}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_group_prayer_notification(self, prayer_data):
        """Send notification to prayer groups"""
        topic = 'prayer_warriors'
        
        message = messaging.Message(
            notification=messaging.Notification(
                title="🕊️ Group Prayer Request",
                body=f"New {prayer_data['prayer_type']} request needs collective prayers",
            ),
            topic=topic,
            data={
                'action': 'GROUP_PRAYER',
                'prayer_id': str(prayer_data['prayer_id']),
                'prayer_count': str(prayer_data.get('prayer_count', 0))
            }
        )
        
        response = messaging.send(message)
        return response
    
    def subscribe_to_topic(self, token, topic='prayer_updates'):
        """Subscribe user to prayer updates"""
        response = messaging.subscribe_to_topic([token], topic)
        return response
    
    def schedule_daily_prayer_reminder(self, user_token, prayer_time):
        """Schedule daily prayer reminders"""
        # This would integrate with Cloud Functions for scheduling
        pass

# Streamlit UI Integration
def notification_settings():
    st.header("🔔 Push Notification Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_notifications = st.checkbox("Enable Push Notifications", True)
        prayer_alerts = st.checkbox("New Prayer Alerts", True)
        prayer_answered = st.checkbox("Prayer Answered Alerts", True)
        daily_reminder = st.checkbox("Daily Prayer Reminder", False)
    
    with col2:
        if daily_reminder:
            reminder_time = st.time_input("Reminder Time")
            reminder_days = st.multiselect(
                "Days",
                ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                default=["Mon", "Wed", "Fri", "Sun"]
            )
        
        vibration = st.checkbox("Vibration", True)
        sound = st.checkbox("Sound", True)
        led_light = st.checkbox("LED Notification", False)
    
    # Test Notification Button
    if st.button("📱 Test Notification"):
        notifier = PrayerNotifications()
        test_data = {
            'user_name': 'Test User',
            'prayer_type': 'General Prayer',
            'prayer_id': 999,
            'timestamp': '2024-01-01 12:00:00'
        }
        
        # In real app, get token from user database
        # test_token = get_user_token(user_id)
        
        with st.spinner("Sending test notification..."):
            result = notifier.send_prayer_notification("test_token", test_data)
            if result['success']:
                st.success("Test notification sent successfully!")
            else:
                st.error(f"Failed: {result['error']}")
    
    return {
        'enabled': enable_notifications,
        'alerts': prayer_alerts,
        'answered': prayer_answered,
        'daily_reminder': daily_reminder
    }
```
