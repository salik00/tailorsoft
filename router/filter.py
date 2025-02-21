from fastapi import APIRouter,FastAPI,Query, Depends, status,HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from database import get_db
import models, schemas

router = APIRouter(prefix="/order",
                   tags=(["FILTERS"]))

@router.get("/filters")
async def filter_orders(
    search_by: str = Query(...),
    bill_no: Optional[str] = None,
    created_from: Optional[date] = None,
    created_to: Optional[date] = None,
    delivered_from: Optional[date] = None,
    delivered_to: Optional[date] = None,
    order_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if search_by == "bill_no":
        if not bill_no:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"bill_no is required")
        query = db.query(models.Order).filter(models.Order.bill_no == bill_no)
        
    elif search_by == "created_at":
        if created_from and created_to:
            query = db.query.filter(models.Order.created_at >= created_from, models.Order.created_at <= created_to)
        elif created_from:
            query = db.query(models.Order).filter(models.Order.created_at >= created_from)
        elif created_to:
            query = db.query(models.Order).filter(models.Order.created_at <= created_to)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one of created_from or created_to is required")

    elif search_by == "delivered_at":
        if delivered_from and delivered_to:
            query = db.query(models.Order).filter(models.Order.delivered_at >= delivered_from, models.Order.delivered_at <= delivered_to)
        elif delivered_from:
            query = db.query(models.Order).filter(models.Order.delivered_at >= delivered_from)
        elif delivered_to:
            query = db.query(models.Order).filter(models.Order.delivered_at <= delivered_to)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one of delivered_from or delivered_to is required")

    elif search_by == "order_status":
        if not order_status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="order_status is required")
        query = db.query(models.Order).filter(models.Order.order_status == order_status)

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid search_by value")

    results = query.all()
    return results