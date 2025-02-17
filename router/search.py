from sqlalchemy import func
from fastapi import Query, APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas,models

router = APIRouter(prefix="/search", tags=["SEARCH"])

@router.get("/order", response_model=List[schemas.GetOrderResponse])
def search_orders(query: str, db:Session = Depends(get_db), 
                #   query: str = Query(..., description="Search by Customer Name"),
                  limit: int = 2,
                  offset: int = 0
                  ):
    search_query = func.to_tsquery('english', query)
    results = db.query(
        models.Order.id.label("order_id"),
        models.Order.customer_name,
        models.Order.delivery_date,
        models.Order.created_at,
        models.Order.is_urgent,
        models.Order.extra_info,
        models.Order.total_quantity,
        models.Order.total_price,
        models.Order.order_status
    ).filter(models.Order.search_vector.op("@@")(func.to_tsquery("english",f"{query}:*"))).order_by(models.Order.created_at.desc()).limit(limit).offset(offset).all()
    
    if not results:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"Not found any content related to this...")
    print("querying:", search_query)
    print("rsults:", results)    
    return results
