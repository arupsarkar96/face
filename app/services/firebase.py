import logging

import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials

cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred)

def firebase_send_to_token(registration_token: str, title: str, body: str) -> bool:
    """
    Sends an FCM push notification to a device using its registration token.

    Args:
        registration_token (str): FCM registration token for the device.
        title (str): Title of the notification.
        body (str): Body text of the notification.

    Returns:
        bool: True if message sent successfully, False otherwise.
    """
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=registration_token,
        )
        response = messaging.send(message)
        logging.info(f"Successfully sent message: {response}")
        return True
    except Exception as e:
        logging.error(f"Failed to send FCM message: {e}")
        return False
