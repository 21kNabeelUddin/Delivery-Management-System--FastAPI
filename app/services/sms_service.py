from typing import Optional
from app.core.config import settings


class SMSService:
    def __init__(self):
        self.provider = settings.SMS_PROVIDER
        self.api_key = settings.SMS_API_KEY
        self.api_secret = settings.SMS_API_SECRET
        self.from_number = settings.SMS_FROM_NUMBER
    
    def send_sms(self, to_phone: str, message: str) -> bool:
        """
        Send an SMS to the specified phone number.
        
        Args:
            to_phone: Recipient phone number (E.164 format)
            message: SMS message content
            
        Returns:
            bool: True if SMS was sent successfully, False otherwise
        """
        if not all([self.provider, self.api_key]):
            print(f"SMS not configured. Would send to {to_phone}: {message}")
            return False
        
        try:
            if self.provider == "twilio":
                return self._send_via_twilio(to_phone, message)
            elif self.provider == "aws_sns":
                return self._send_via_aws_sns(to_phone, message)
            else:
                print(f"Unknown SMS provider: {self.provider}")
                return False
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return False
    
    def _send_via_twilio(self, to_phone: str, message: str) -> bool:
        """Send SMS via Twilio."""
        try:
            from twilio.rest import Client
            client = Client(self.api_key, self.api_secret)
            message = client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_phone
            )
            return message.sid is not None
        except ImportError:
            print("Twilio library not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            print(f"Twilio error: {str(e)}")
            return False
    
    def _send_via_aws_sns(self, to_phone: str, message: str) -> bool:
        """Send SMS via AWS SNS."""
        try:
            import boto3
            sns = boto3.client(
                'sns',
                aws_access_key_id=self.api_key,
                aws_secret_access_key=self.api_secret
            )
            response = sns.publish(
                PhoneNumber=to_phone,
                Message=message
            )
            return 'MessageId' in response
        except ImportError:
            print("boto3 library not installed. Install with: pip install boto3")
            return False
        except Exception as e:
            print(f"AWS SNS error: {str(e)}")
            return False
    
    def send_delivery_notification(self, to_phone: str, delivery_info: dict) -> bool:
        """Send delivery status notification SMS."""
        message = f"Delivery Update: {delivery_info.get('item_name')} - Status: {delivery_info.get('status')} - Tracking: {delivery_info.get('tracking_number')}"
        return self.send_sms(to_phone, message)


sms_service = SMSService()

