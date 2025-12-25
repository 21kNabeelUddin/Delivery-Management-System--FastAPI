from fastapi import APIRouter, status, HTTPException, Depends, Form
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.delivery import Delivery
from app.models.user import User
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate, ShowDelivery
from app.api.dependencies import get_current_user
from app.services.email_service import email_service
from app.services.sms_service import sms_service
from app.tasks.sms_tasks import send_delivery_notification_sms_task

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("/{delivery_id}", status_code=status.HTTP_200_OK, response_model=ShowDelivery)
def show_delivery(delivery_id: int, db: Session = Depends(get_db)):
    db_delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    return db_delivery


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_delivery(
    item_name: str = Form(..., description="Name of the item"),
    destination: str = Form(..., description="Delivery destination"),
    status: str = Form(..., description="Delivery status"),
    tracking_number: str = Form(..., description="Tracking number"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_delivery = Delivery(
        item_name=item_name,
        destination=destination,
        status=status,
        tracking_number=tracking_number,
        user_id=current_user.id
    )
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    
    delivery_info = {
        "item_name": db_delivery.item_name,
        "destination": db_delivery.destination,
        "status": db_delivery.status,
        "tracking_number": db_delivery.tracking_number
    }
    email_service.send_delivery_notification(current_user.email, delivery_info)
    
    return {"message": "Delivery created successfully", "delivery": {"id": db_delivery.id, "item_name": db_delivery.item_name, "destination": db_delivery.destination, "status": db_delivery.status, "tracking_number": db_delivery.tracking_number}}


@router.put("/{delivery_id}", status_code=status.HTTP_200_OK)
def update_delivery(
    delivery_id: int,
    item_name: str = Form(None, description="Name of the item"),
    destination: str = Form(None, description="Delivery destination"),
    status: str = Form(None, description="Delivery status"),
    tracking_number: str = Form(None, description="Tracking number"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    
    if db_delivery.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this delivery")
    
    if item_name is not None:
        db_delivery.item_name = item_name
    if destination is not None:
        db_delivery.destination = destination
    if status is not None:
        db_delivery.status = status
    if tracking_number is not None:
        db_delivery.tracking_number = tracking_number
    
    db.commit()
    db.refresh(db_delivery)
    
    delivery_info = {
        "item_name": db_delivery.item_name,
        "destination": db_delivery.destination,
        "status": db_delivery.status,
        "tracking_number": db_delivery.tracking_number
    }
    email_service.send_delivery_notification(current_user.email, delivery_info)
    
    return {"message": f"Delivery with id {delivery_id} updated successfully", "delivery": {"id": db_delivery.id, "item_name": db_delivery.item_name, "destination": db_delivery.destination, "status": db_delivery.status, "tracking_number": db_delivery.tracking_number}}


@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(delivery_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not db_delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery not found")
    
    if db_delivery.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this delivery")
    
    db.delete(db_delivery)
    db.commit()
    return {"message": f"Delivery with id {delivery_id} deleted successfully"}

