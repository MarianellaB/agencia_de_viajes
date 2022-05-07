from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.bd import Base
from app.core import hashing

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(255))
    username = Column(String(255), unique=True) 
    password = Column(String(255))

    booking = relationship("Booking", back_populates="customer")

    def __init__(self, fullname, username, password, *args, **kwargs):
        self.fullname = fullname
        self.username = username
        self.password = hashing.get_password_hash(password)
    
    def check_password(self, password):
        return hashing.verify_password(self.password, password)