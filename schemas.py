from pydantic import BaseModel
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
    quantity: int
    price: int
    measurement: Optional[Dict[str, int]] = None
    design: Optional[Dict[str, str]] = None
    extra_info: Optional[str] = None

class ItemCreateResponse(ItemCreate):
    id: int
    order_id: int
    class Config:
        from_attributes = True
        
class OrderBase(BaseModel):
    customer_name: str
    contact_no: str
    address: str
    delivery_date: str
    is_urgent: bool = False
    extra_info: Optional[str]
    order_status: bool = False
    # total_quantity: Optional[int]
    # total_price: Optional[int]
    items: List[ItemCreate]

class OrderCreate(OrderBase):
    pass

class OrderCreateResponse(OrderBase):
    id: int
    total_quantity: int
    total_price: int
    items: List[ItemCreateResponse]
    # order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

class GetOrderResponse(BaseModel):
    order_id: int
    customer_name: str
    delivery_date: str
    created_at: datetime
    is_urgent: bool 
    extra_info: str
    total_quantity: int
    total_price: int
    order_status: bool

# class ItemTypeBase(BaseModel):
#     name: str

# class ItemTypeCreate(ItemTypeBase):
#     pass

# class ItemTypeResponse(ItemTypeBase):
#     id: int
#     class Config:
#         from_attributes = True 

#-----------------------
#  measurementschema
#----------------------
# class MeasurementBase(BaseModel):
#     order_item_id: int
#     item_type_id: int
    
#     #shirt measurement
#     shirt_collar: Optional[str] = None
#     shirt_sleeve: Optional[str] = None
#     shirt_height: Optional[str] = None
#     #pant measurement
#     pant_mohri: Optional[str] = None
#     pant_hip: Optional[str] = None
#     pant_waist: Optional[str] = None
#      #coat measurement
#     coat_collar: Optional[str] = None
#     coat_sleeve: Optional[str] = None
#     coat_waist: Optional[str] = None

# class MeasurementCreate(MeasurementBase):
#     pass

# class MeasurementResponse(MeasurementBase):
#     id: int 
#     class Config:
#         from_attributes = True

# #---------------------
# #   DESIGN SCHEMA
# #---------------------
# class DesignBase(BaseModel):
#     order_item_id: int
#     item_type_id: int
    
#     #shirt measurement
#     plate: Optional[str] = None
#     round: Optional[str] = None
#     #pant design
#     loosefit: Optional[str] = None
#     slimfit: Optional[str] = None
#      #coat measurement
#     british: Optional[str] = None
#     american: Optional[str] = None

# class DesignCreate(DesignBase):
#     pass

# class DesignResponse(DesignBase):
#     id: int
#     class Config:
#         from_attributes = True

# # ----------- ORDER SCHEMAS----------



