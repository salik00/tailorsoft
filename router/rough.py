from fastapi import FastAPI, HTTPException, APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import models,schemas
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
import os
import shutil
import json

router = APIRouter(prefix ="/order", tags=["ORDERS"])

UPLOAD_FOLDER = "uploads/images"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@router.post("/createorder", response_model=schemas.OrderCreateResponse)
async def create_order(
    order: str = File(...),  # Accept order as a JSON string
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Parse JSON order data
        order_data = json.loads(order)
        order_obj = schemas.OrderCreate(**order_data)

        total_quantity = sum(item.quantity for item in order_obj.items)
        total_price = sum(item.price * item.quantity for item in order_obj.items)
    
        image_path = None
        if image:
            image_filename = os.path.join(UPLOAD_FOLDER, image.filename)
            with open(image_filename, "wb") as buffer:
                shutil.copyfileobject(image.file, buffer)
            image_path = image_filename 
        
        db_order = models.Order(
            customer_name=order.customer_name,
            contact_no=order.contact_no,
            address=order.address,
            delivery_date=order.delivery_date,
            is_urgent=order.is_urgent,
            extra_info=order.extra_info,
            total_price=total_price,
            total_quantity=total_quantity,
            image_path = image_path,
            order_status=order.order_status
        )
        for item_data in order.items:
            item = models.OrderItem(
                item_name= item_data.item_name,
                quantity= item_data.quantity,
                price= item_data.price,
                extra_info= item_data.extra_info,
                order = db_order
            )
            db.add(item)
    
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        return db_order
    
    except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format for 'order' field.")

@router.get("/getorder", response_model=List[schemas.GetOrderResponse])
def get_order(db:Session= Depends(get_db),limit:int=3, offset:int=0):
    result = db.query(
        models.Order.id.label("order_id"),
        models.Order.customer_name,
        models.Order.delivery_date,
        models.Order.created_at,
        models.Order.is_urgent,
        models.Order.extra_info,
        models.Order.total_quantity,
        models.Order.total_price,   
        models.Order.order_status
    ).order_by(models.Order.created_at.desc()).limit(limit).offset(offset).all()
    return result
