from sqlmodel import Session, select
from typing import List, Optional
from application.backend.app.models.transport_models import *
from datetime import time, date
from application.backend.app.models.transport_models import TransportType, DaysOfWeek, EmployeePosition, ChangeReason

class TransportController:
    def __init__(self, session: Session):
        self.session = session

    # Методы для остановок
    def create_stop(self, name: str, latitude: float, longitude: float, has_pavilion: bool = False) -> Stop:
        stop = Stop(name=name, latitude=latitude, longitude=longitude, has_pavilion=has_pavilion)
        self.session.add(stop)
        self.session.commit()
        self.session.refresh(stop)
        return stop

    def get_all_stops(self) -> List[Stop]:
        statement = select(Stop)
        return self.session.exec(statement).all()

    # Методы для маршрутов
    def create_route(self, route_number: str, transport_type: str, start_district: str, end_district: str,
                    total_travel_time: int, carrier_id: int) -> Route:
        route = Route(
            route_number=route_number,
            transport_type=transport_type,
            start_district=start_district,
            end_district=end_district,
            total_travel_time=total_travel_time,
            carrier_id=carrier_id
        )
        self.session.add(route)
        self.session.commit()
        self.session.refresh(route)
        return route

    def get_routes_by_district(self, district: str) -> List[Route]:
        statement = select(Route).where(
            (Route.start_district == district) | (Route.end_district == district)
        )
        return self.session.exec(statement).all()

    # Методы для перевозчиков
    def create_carrier(self, name: str, contact_phone: Optional[str] = None,
                      email: Optional[str] = None) -> Carrier:
        carrier = Carrier(name=name, contact_phone=contact_phone, email=email)
        self.session.add(carrier)
        self.session.commit()
        self.session.refresh(carrier)
        return carrier

    # Методы для связей маршрут-остановка
    def add_stop_to_route(self, route_id: int, stop_id: int, stop_order: int, arrival_time: time) -> RouteStop:
        route_stop = RouteStop(
            route_id=route_id,
            stop_id=stop_id,
            stop_order=stop_order,
            arrival_time=arrival_time
        )
        self.session.add(route_stop)
        self.session.commit()
        self.session.refresh(route_stop)
        return route_stop

    def get_route_stops(self, route_id: int) -> List[RouteStop]:
        statement = select(RouteStop).where(RouteStop.route_id == route_id).order_by(RouteStop.stop_order)
        return self.session.exec(statement).all()

    def get_all_routes(self) -> List[Route]:
        statement = select(Route)
        return self.session.exec(statement).all()