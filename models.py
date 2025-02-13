from database import Base
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, nullable=False)
    customer_name = Column(String, nullable=False)
    contact_no = Column(String, nullable=False)
    address = Column(String, nullable=False)
    delivery_date = Column(String, nullable=False)
    is_urgent = Column(Boolean, default=False)
    extra_info = Column(Text, nullable=True)
    total_price = Column(Integer, nullable=False)
    total_quantity = Column(Integer,nullable=False)
    order_status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    items = relationship("OrderItem", back_populates="order")

# class ItemType(Base):
#     __tablename__ = "item_type"
    
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String, nullable=False)
    
class OrderItem(Base):
    __tablename__ = "order_item"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    # item_type_id = Column(Integer, ForeignKey("item_type.id"), nullable=False)
    item_name = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Integer)
    measurement = Column(JSON, nullable=True)
    design = Column(JSON, nullable=True)
    extra_info = Column(String, nullable=True)
    
    order = relationship("Order", back_populates="items")
    # item_type = relationship("ItemType")
    # measurement = relationship("Measurement", uselist=False, back_populates="order_item")
    # design = relationship("Design", uselist=False, back_populates="order_item")

# class Measurement(Base):
#     __tablename__ = "measurement"
    
#     id = Column(Integer, primary_key=True, nullable=False)
#     order_item_id = Column(Integer, ForeignKey("order_item.id"), nullable=False)
#     item_type_id = Column(Integer, ForeignKey("item_type.id"), nullable=False)
    
#     #shirt measurement
#     shirt_collar = Column(String, nullable=True)
#     shirt_sleeve = Column(String, nullable=True)
#     shirt_height = Column(String, nullable=True)
#     #pant measurement
#     pant_mohri = Column(String, nullable=True)
#     pant_hip = Column(String, nullable=True)
#     pant_waist = Column(String, nullable=True)
#      #coat measurement
#     coat_collar = Column(String, nullable=True)
#     coat_sleeve = Column(String, nullable=True)
#     coat_waist = Column(String, nullable=True)
    
#     order_item = relationship("OrderItem", back_populates="measurement")

# class Design(Base):
#     __tablename__ = "design"
    
#     id = Column(Integer, primary_key=True, nullable=False)
#     order_item_id = Column(Integer, ForeignKey("order_item.id"), nullable=False)
#     item_type_id = Column(Integer, ForeignKey("item_type.id"), nullable=False)
    
#     #shirt design
#     plate = Column(String, nullable=True)
#     round = Column(String, nullable=True)

#     #pant dsign
#     loosefit = Column(String, nullable=True)
#     slimfit = Column(String, nullable=True)

#     #coat design
#     british = Column(String, nullable=True)
#     american = Column(String, nullable=True)
    
#     order_item = relationship("OrderItem", back_populates="design")