from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from datetime import date
from . import models
from . import schema
from app.booking import models as booking_models


async def get_all_flights(bd_session: Session) -> List[models.Flight]:
    flights = bd_session.query(models.Flight).all()
    return flights

async def get_flights(departureAirportCode: str, arrivalAirportCode: str, departureDate: date, bd_session: Session) -> List[models.Flight]:
    dac = bd_session.query(models.Flight).filter(models.Flight.departureAirportCode == departureAirportCode).all()
    if not dac: 
        raise HTTPException(status_code=404, detail="Departure airport code not found")   
    aac = bd_session.query(models.Flight).filter(models.Flight.arrivalAirportCode == arrivalAirportCode).all()
    if not aac: 
        raise HTTPException(status_code=404, detail="Arrival airport code not found")

    flights = bd_session.query(models.Flight).filter(models.Flight.departureAirportCode == departureAirportCode, 
                                                     models.Flight.arrivalAirportCode == arrivalAirportCode,
                                                     func.date(models.Flight.departureDate) == departureDate).all()
    return flights                                   # La función func.date() extrae el date de un datetime.
                                                     # En este caso, extrae el date de departureDate (datetime)

async def get_flights_by_departureairportcode_and_departuredate(departureAirportCode: str, departureDate: date, bd_session: Session) -> List[models.Flight]:
    dac = bd_session.query(models.Flight).filter(models.Flight.departureAirportCode == departureAirportCode).all()
    if not dac: 
        raise HTTPException(status_code=404, detail="Departure airport code not found")

    if departureDate:
        flights = bd_session.query(models.Flight).filter(models.Flight.departureAirportCode == departureAirportCode, 
                                                     func.date(models.Flight.departureDate) == departureDate).all()
    else:
        flights = dac
    
    return flights

async def create_new_flight(flight: schema.FlightCreate, bd_session: Session) -> models.Flight:
    new_flight = models.Flight(**flight.dict())
    bd_session.add(new_flight)
    bd_session.commit()
    bd_session.refresh(new_flight)

    return new_flight

async def update_flight(flight_id: int, flight: schema.FlightUpdate, bd_session: Session):
    updated_flight = models.Flight(**flight.dict())
    bd_session.query(models.Flight).filter(models.Flight.id == flight_id).update(
                                           {
                                               models.Flight.id: flight_id,
                                               models.Flight.departureDate: updated_flight.departureDate,
                                               models.Flight.departureAirportCode: updated_flight.departureAirportCode,
                                               models.Flight.departureAirportName: updated_flight.departureAirportName,
                                               models.Flight.departureCity: updated_flight.departureCity,
                                               models.Flight.departureLocale: updated_flight.departureLocale,
                                               models.Flight.arrivalDate: updated_flight.arrivalDate,
                                               models.Flight.arrivalAirportCode: updated_flight.arrivalAirportCode,
                                               models.Flight.arrivalAirportName: updated_flight.arrivalAirportName,
                                               models.Flight.arrivalCity: updated_flight.arrivalCity,
                                               models.Flight.arrivalLocale: updated_flight.arrivalLocale,
                                               models.Flight.ticketPrice: updated_flight.ticketPrice,
                                               models.Flight.ticketCurrency: updated_flight.ticketCurrency,
                                               models.Flight.flightNumber: updated_flight.flightNumber,
                                               models.Flight.seatCapacity: updated_flight.seatCapacity 
                                           }, synchronize_session=False)
    bd_session.commit()
    return updated_flight

async def delete_flight(flight_id: int, bd_session: Session):
   
    booking = bd_session.query(booking_models.Booking).filter(booking_models.Booking.outboundFlight_id == flight_id).all()
    if booking:
        for b in booking:
            bd_session.delete(b)
    bd_session.commit()
    bd_session.query(models.Flight).filter(models.Flight.id == flight_id).delete()
    bd_session.commit()