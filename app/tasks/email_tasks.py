from app.tasks.celery_app import celery_app
from app.services.email_service import email_service


@celery_app.task(name="send_email")
def send_email_task(to_email: str, subject: str, body: str, html_body: str = None):
    """Celery task to send email asynchronously."""
    return email_service.send_email(to_email, subject, body, html_body)


@celery_app.task(name="send_verification_email")
def send_verification_email_task(to_email: str, verification_token: str):
    """Celery task to send verification email asynchronously."""
    return email_service.send_verification_email(to_email, verification_token)


@celery_app.task(name="send_password_reset_email")
def send_password_reset_email_task(to_email: str, reset_token: str):
    """Celery task to send password reset email asynchronously."""
    return email_service.send_password_reset_email(to_email, reset_token)


@celery_app.task(name="send_delivery_notification_email")
def send_delivery_notification_email_task(to_email: str, delivery_info: dict):
    """Celery task to send delivery notification email asynchronously."""
    return email_service.send_delivery_notification(to_email, delivery_info)

