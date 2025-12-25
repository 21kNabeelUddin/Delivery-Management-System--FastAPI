from app.tasks.celery_app import celery_app
from app.services.sms_service import sms_service


@celery_app.task(name="send_sms")
def send_sms_task(to_phone: str, message: str):
    """Celery task to send SMS asynchronously."""
    return sms_service.send_sms(to_phone, message)


@celery_app.task(name="send_delivery_notification_sms")
def send_delivery_notification_sms_task(to_phone: str, delivery_info: dict):
    """Celery task to send delivery notification SMS asynchronously."""
    return sms_service.send_delivery_notification(to_phone, delivery_info)

