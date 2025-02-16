from database import Base
from sqlalchemy import Index,Column, String, Integer, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import TSVECTOR

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
    search_vector = Column(TSVECTOR)
    items = relationship("OrderItem", back_populates="order")
   
    __table_args__ = (
        Index("idx_order_search_vector", "search_vector", postgresql_using="gin"),
    )
    
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
