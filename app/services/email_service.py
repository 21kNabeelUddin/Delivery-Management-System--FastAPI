from typing import Optional
from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
    
    def send_email(self, to_email: str, subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """
        Send an email to the specified recipient.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: Optional HTML email body
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not all([self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_password]):
            print(f"Email not configured. Would send to {to_email}: {subject}")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_from or self.smtp_user
            msg['To'] = to_email
            
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def send_verification_email(self, to_email: str, verification_token: str) -> bool:
        """Send email verification email."""
        verification_url = f"http://localhost:8000/api/auth/verify-email?token={verification_token}"
        subject = "Verify Your Email Address"
        body = f"Please click the following link to verify your email: {verification_url}"
        html_body = f"""
        <html>
          <body>
            <h2>Verify Your Email Address</h2>
            <p>Please click the following link to verify your email address:</p>
            <a href="{verification_url}">Verify Email</a>
            <p>Or copy and paste this URL into your browser: {verification_url}</p>
          </body>
        </html>
        """
        return self.send_email(to_email, subject, body, html_body)
    
    def send_password_reset_email(self, to_email: str, reset_token: str) -> bool:
        """Send password reset email."""
        reset_url = f"http://localhost:8000/api/auth/reset-password?token={reset_token}"
        subject = "Reset Your Password"
        body = f"Please click the following link to reset your password: {reset_url}"
        html_body = f"""
        <html>
          <body>
            <h2>Reset Your Password</h2>
            <p>Please click the following link to reset your password:</p>
            <a href="{reset_url}">Reset Password</a>
            <p>Or copy and paste this URL into your browser: {reset_url}</p>
            <p>This link will expire in 1 hour.</p>
          </body>
        </html>
        """
        return self.send_email(to_email, subject, body, html_body)
    
    def send_delivery_notification(self, to_email: str, delivery_info: dict) -> bool:
        """Send delivery status notification email."""
        subject = f"Delivery Update: {delivery_info.get('item_name', 'Your Delivery')}"
        body = f"""
        Your delivery has been updated:
        
        Item: {delivery_info.get('item_name')}
        Destination: {delivery_info.get('destination')}
        Status: {delivery_info.get('status')}
        Tracking Number: {delivery_info.get('tracking_number')}
        """
        html_body = f"""
        <html>
          <body>
            <h2>Delivery Update</h2>
            <p>Your delivery has been updated:</p>
            <ul>
              <li><strong>Item:</strong> {delivery_info.get('item_name')}</li>
              <li><strong>Destination:</strong> {delivery_info.get('destination')}</li>
              <li><strong>Status:</strong> {delivery_info.get('status')}</li>
              <li><strong>Tracking Number:</strong> {delivery_info.get('tracking_number')}</li>
            </ul>
          </body>
        </html>
        """
        return self.send_email(to_email, subject, body, html_body)


email_service = EmailService()

