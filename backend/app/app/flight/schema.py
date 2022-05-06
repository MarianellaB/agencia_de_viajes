from pydantic import BaseModel, constr
from datetime import datetime

class FlightBase(BaseModel):
    departureDate: datetime
    departureAirportCode: constr(max_length=40)
    departureAirportName: str
    departureCity: str
    departureLocale: str
    arrivalDate: datetime
    arrivalAirportCode: constr(max_length=40)
    arrivalAirportName: str
    arrivalCity: str
    arrivalLocale: str
    ticketPrice: int
    ticketCurrency: str
    flightNumber: int
    seatCapacity: int

class FlightCreate(FlightBase):
    pass

class FlightUpdate(FlightBase):
    pass

class FlightInDBBase(FlightBase):
    id: int

    class Config:
        orm_mode = True

class Flight(FlightInDBBase):
    pass

class FightInDB(FlightInDBBase):
    pass