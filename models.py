from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    normalized_name = Column(String)
    price = Column(Float)
    rating = Column(Float)
    source = Column(String)
    url = Column(String, unique=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
