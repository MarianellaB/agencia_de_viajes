from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database.bd import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key = True, autoincrement = True)
    departureDate = Column(DateTime)
    departureAirportCode = Column(String(60))
    departureAirportName = Column(String(100))
    departureCity = Column(String(255))
    departureLocale = Column(String(255))
    arrivalDate = Column(DateTime)
    arrivalAirportCode = Column(String(60))
    arrivalAirportName = Column(String(100))
    arrivalCity = Column(String(255))
    arrivalLocale = Column(String(255))
    ticketPrice = Column(Integer)
    ticketCurrency = Column(String(60))
    flightNumber = Column(Integer)
    seatCapacity = Column(Integer)
    booking = relationship("Booking", back_populates="flight")

