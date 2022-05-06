from datetime import date
import string
from sqlalchemy import column, integer, String, Boolean
from sqlalchemy.orm import relationship
from database.Session import Base


class flight(Base):
    __tablename__="flight"
    id = column(integer, primary_key=True, autoincrement = True)
    departuredate= column(String(50))
    departureAirportCode= column(String(50))
    departureAirportName= column(String(50))r
    departureCity= column(String(50))
    departureLocale= column(String(50))
    arrivalDate= column(String(50))
    arrivalAirportCode= column(String(50))
    arrivalAirportName= column(String(50))
    arrivalCity= column(String(50))
    arrivalLocale= column(String(50))
    ticketPrice= column(integer)
    ticketCurrency= column(String(50))
    flightNumber= column(integer)
    seatCapacity= column(integer)
    
    