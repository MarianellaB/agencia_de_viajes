from logging import StreamHandler
from re import A
from tokenize import String
from typing_extensions import StrictTypeGuard
from unittest.mock import DEFAULT
from xmlrpc.client import Boolean
from xxlimited import Str


class flight:
    id: int
    departuredate: Str
    departureAirportCode: str
    departureAirportName: Str
    departureCity: str
    departureLocale:str
    arrivalDate:str
    arrivalAirportCode:str
    arrivalAirportName:str
    arrivalCity:str
    arrivalLocale:str
    ticketPrice:int
    ticketCurrency:str
    flightNumber: int
    seatCapacity:int
    
    

def BookingStatus(a):
    if a==0:
        return "UNCONFIRMED"
    elif a==1:
        return "CONFIRMED"
    elif a==2:
        return "CANCELLED"
    else:
        print("numero incorrecto. el estado de validacion no es correcto")
       
class User:
    id: int
    fullname: String
    username: String 
    password: String

class Booking:
    id: int
    status: BookingStatus
    outboundFlight: flight
    paymentToken: String
    checkedIn: Boolean
    customer: User
    createdAt: String
    bookingReference: String
    
