from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import List, Dict

# ----------- USER SCHEMAS ---------

class UserCreate(BaseModel):
    username: str
    password: str
    is_superuser: Optional[bool]

class UserOut(BaseModel):
    id: int
    username: str 
    created_at: datetime
    is_superuser: bool
        
class UserResponse(BaseModel):
    id: int
    username: str
    is_superuser: bool
    created_at: datetime
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserToken(BaseModel):
    access_token: str
    token_type: str
    
class ItemCreate(BaseModel):
    item_name: str 
    # = Field(alias="name")
    quantity: int
    price: int
    extra_info: Optional[str] = None

class ItemCreateResponse(ItemCreate):
    id: int
    order_id: int
    class Config:
        from_attributes = True
        
class OrderBase(BaseModel):
    customer_name: str
    contact_no: str
    created_at: datetime
    delivery_date: datetime
    order_status: str 
    bill_no: int
    items: List[ItemCreate]


class OrderCreate(OrderBase):
    pass

class OrderCreateResponse(OrderBase):
    id: int
    total_quantity: int
    total_price: int
    image_path: Optional[str]
    items: List[ItemCreateResponse]
    
    class Config:
        from_attributes = True

class GetOrderResponse(BaseModel):
    order_id: int
    customer_name: str
    delivery_date: str
    created_at: datetime
    total_quantity: int
    total_price: int
    order_status: str


