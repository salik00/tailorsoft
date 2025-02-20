from fastapi import FastAPI, Form, HTTPException, APIRouter, Depends, UploadFile, File
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
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    total_quantity = sum(item.quantity for item in order.items)
    total_price = sum(item.price * item.quantity for item in order.items)

    db_order = models.Order(
        customer_name=order.customer_name,
        contact_no=order.contact_no,
        created_at=order.created_at,
        delivery_date=order.delivery_date,
        total_price=total_price,
        total_quantity=total_quantity,
        order_status=order.order_status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# @router.post("/createorder", response_model=schemas.OrderCreateResponse)
# async def create_order(
#     order: str= Form(...),  # Accept order as a JSON string
    
#     image: UploadFile = File(None),
#     db: Session = Depends(get_db)   
# ):
#     # print(order)
#     # return
#     try:
#         # Parse JSON order data
#         order_data = json.loads(order)
#         order_obj = schemas.OrderCreate(**order_data)

#         total_quantity = sum(item.quantity for item in order_obj.items)
#         total_price = sum(item.price * item.quantity for item in order_obj.items)
    
#         image_path = None
#         if image and image.filename:
#             print(f"received image : {image.filename}")
            
#             image_extension = os.path.splitext(image.filename)[1]
#             new_filename = f"order_{order_obj.customer_name}_{order_obj.contact_no}{image_extension}"
#             image_filename = os.path.join(UPLOAD_FOLDER, new_filename)
         
#             try:
#                 with open(image_filename, "wb") as buffer:
#                     shutil.copyfileobj(image.file, buffer)  # Save file
                
#                 print(f"Image saved successfully at: {image_filename}")
#                 image_path = image_filename  # Assign saved path

#             except Exception as e:
#                     print(f"Error saving image: {str(e)}")
#                     raise HTTPException(status_code=500, detail="Failed to save image")
        
#         db_order = models.Order(
#             customer_name=order_obj.customer_name,
#             contact_no=order_obj.contact_no,
#             created_at = order_obj.created_at,
#             delivery_date=order_obj.delivery_date,
#             total_price=total_price,
#             total_quantity=total_quantity,
#             image_path = image_path,
#             order_status=order_obj.order_status
#         )
#         db.add(db_order)
#         db.commit()
#         db.refresh(db_order)
        
#         for item_data in order_obj.items:
#             item = models.OrderItem(
#                 item_name= item_data.item_name,
#                 quantity= item_data.quantity,
#                 price= item_data.price,
#                 order = db_order
#             )
#             db.add(item)
    
#         # db.add(db_order)
#         db.commit()
#         db.refresh(db_order)
#         if image:
#             db_order.image_path = image_path
#             db.commit()
#             db.refresh(db_order)
#          # ✅ Debugging: Print final stored image path
#         print(f"✅ Final Image Path in DB: {db_order.image_path}")
#         print(f"Stored Image Path: {db_order.image_path}")  # Debugging

#         return db_order
    
#     except json.JSONDecodeError:
#             raise HTTPException(status_code=400, detail="Invalid JSON format for 'order' field.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
# @router.get("/getorder", response_model=List[schemas.GetOrderResponse])
# def get_order(db:Session= Depends(get_db),limit:int=3, offset:int=0):
#     result = db.query(
#         models.Order.id.label("order_id"),
#         models.Order.customer_name,
#         models.Order.delivery_date,
#         models.Order.created_at,
#         models.Order.total_quantity,
#         models.Order.total_price,   
#         models.Order.image_path,
#         models.Order.order_status
#     ).order_by(models.Order.created_at.desc()).limit(limit).offset(offset).all()
#     return result
