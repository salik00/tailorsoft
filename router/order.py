from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import models,schemas,database
from database import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

router = APIRouter(prefix ="/order", tags=["ORDERS"])

@router.post("/createorder", response_model= schemas.OrderCreateResponse)
def create_order(order:schemas.OrderCreate, db: Session=Depends(get_db),):
    # Create Order object from the provided data
    
    total_quantity = sum(item.quantity for item in order.items)
    total_price = sum(item.price*item.quantity for item in order.items)
    
    db_order = models.Order(
        customer_name=order.customer_name,
        contact_no=order.contact_no,
        address=order.address,
        delivery_date=order.delivery_date,
        is_urgent=order.is_urgent,
        extra_info=order.extra_info,
        total_price=total_price,
        total_quantity=total_quantity,
        order_status=order.order_status
    )
    for item_data in order.items:
        item = models.OrderItem(
            item_name= item_data.item_name,
            quantity= item_data.quantity,
            price= item_data.price,
            measurement=item_data.measurement,
            design= item_data.design,
            extra_info= item_data.extra_info,
            order = db_order
        )
        db.add(item)
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order

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