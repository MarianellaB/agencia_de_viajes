from fastapi import APIRouter, Depends, status, Response, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import bd
from . import schema
from . import services
from . import validation
from app.core import security
from app.user import schema as user_schema

api_router = APIRouter(tags = ["Catalog"])

@api_router.get("/catalog/all", response_model = List[schema.Flight])
async def get_all_flights(bd_session: Session = Depends(bd.get_bd_session)):
    return await services.get_all_flights(bd_session)

@api_router.get("/catalog/", response_model=List[schema.Flight])
async def get_flights(departureAirportCode: str, arrivalAirportCode: str, departureDate: date, bd_session: Session = Depends(bd.get_bd_session)):
    flights = await services.get_flights(departureAirportCode,arrivalAirportCode,departureDate,bd_session)
    if not flights:
        raise HTTPException(status_code=404, detail="flight(s) not found")

    return flights

@api_router.get("/catalog/{airportCode}", response_model=List[schema.Flight])
async def get_flights_by_airportcode_and_departuredate(airportCode: str, departureDate: Optional[date] = None, bd_session: Session = Depends(bd.get_bd_session)):
    flights = await services.get_flights_by_departureairportcode_and_departuredate(airportCode,departureDate,bd_session)
    if not flights:
        raise HTTPException(status_code=404, detail="flight(s) not found")

    return flights

@api_router.post("/catalog/", status_code = status.HTTP_201_CREATED, response_model=schema.Flight)
async def create_flight(flight_in: schema.FlightCreate, bd_session: Session = Depends(bd.get_bd_session),
                        current_user: user_schema.User = Depends(security.get_current_user)):
    new_flight = await services.create_new_flight(flight_in, bd_session = bd_session)
    return new_flight

@api_router.put('/catalog/{id}', status_code = status.HTTP_201_CREATED)
async def update_flight(id: int, flight: schema.FlightUpdate, bd_session: Session = Depends(bd.get_bd_session),
                        current_user: user_schema.User = Depends(security.get_current_user)):
    existingflight = await validation.verify_flight_exist(id, bd_session)
    if not existingflight:
        raise HTTPException(status_code=404, detail="Non-existent flight")
    
    new_flight = await services.update_flight(id, flight, bd_session)
    return new_flight

@api_router.delete("/catalog/{id}", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def delete_flight(id: int, bd_session: Session = Depends(bd.get_bd_session),
                        current_user: user_schema.User = Depends(security.get_current_user)):
    existingflight = await validation.verify_flight_exist(id, bd_session)
    if not existingflight:
        raise HTTPException(status_code=404, detail="Non-existent flight")
    await services.delete_flight(id, bd_session)

    return "THE FLIGHT AND ALL HIS BOOKINGS HAVE BEEN SUCCESSFULLY DELETED."