from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import time, date, datetime
from enum import Enum

class TransportType(str, Enum):
    TRAIN = "electrotrain"
    BUS = "bus"
    TRAM = "tram"
    TROLLEYBUS = "trolleybus"
    MINIBUS = "minibus"

class DaysOfWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

class EmployeePosition(str, Enum):
    DRIVER = "driver"
    CONDUCTOR = "conductor"

class ChangeReason(str, Enum):
    BREAKDOWN = "breakdown"
    MAINTENANCE = "maintenance"
    WEATHER = "weather"
    STAFF_SHORTAGE = "staff_shortage"
    OTHER = "other"

class Stop(SQLModel, table=True):
    __tablename__ = "stops"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    latitude: float
    longitude: float
    has_pavilion: bool = Field(default=False)

    # Relationships - use absolute paths
    route_stops: List["RouteStop"] = Relationship(back_populates="stop")

class Carrier(SQLModel, table=True):
    __tablename__ = "carriers"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_phone: Optional[str] = None
    email: Optional[str] = None

    # Relationships
    routes: List["Route"] = Relationship(back_populates="carrier")
    employees: List["Employee"] = Relationship(back_populates="carrier")

class Route(SQLModel, table=True):
    __tablename__ = "routes"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    route_number: str
    transport_type: TransportType
    start_district: str
    end_district: str
    total_travel_time: int
    carrier_id: Optional[int] = Field(default=None, foreign_key="carriers.id")

    # Relationships
    carrier: Optional[Carrier] = Relationship(back_populates="routes")
    route_stops: List["RouteStop"] = Relationship(back_populates="route")
    schedules: List["Schedule"] = Relationship(back_populates="route")
    route_days: List["RouteDay"] = Relationship(back_populates="route")

class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    position: EmployeePosition
    hire_date: date
    carrier_id: Optional[int] = Field(default=None, foreign_key="carriers.id")

    # Relationships
    carrier: Optional[Carrier] = Relationship(back_populates="employees")
    employee_schedules: List["EmployeeSchedule"] = Relationship(back_populates="employee")

class RouteStop(SQLModel, table=True):
    __tablename__ = "route_stops"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    route_id: int = Field(foreign_key="routes.id")
    stop_id: int = Field(foreign_key="stops.id")
    stop_order: int
    arrival_time: time

    # Relationships
    route: "Route" = Relationship(back_populates="route_stops")
    stop: "Stop" = Relationship(back_populates="route_stops")

class RouteDay(SQLModel, table=True):
    __tablename__ = "route_days"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    route_id: int = Field(foreign_key="routes.id")
    day_of_week: DaysOfWeek

    # Relationships
    route: "Route" = Relationship(back_populates="route_days")

class Schedule(SQLModel, table=True):
    __tablename__ = "schedules"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    route_id: int = Field(foreign_key="routes.id")
    departure_time: time
    arrival_time: time

    # Relationships
    route: "Route" = Relationship(back_populates="schedules")
    schedule_changes: List["ScheduleChange"] = Relationship(back_populates="schedule")
    employee_schedules: List["EmployeeSchedule"] = Relationship(back_populates="schedule")

class EmployeeSchedule(SQLModel, table=True):
    __tablename__ = "employee_schedules"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employees.id")
    schedule_id: int = Field(foreign_key="schedules.id")
    work_date: date

    # Relationships
    employee: "Employee" = Relationship(back_populates="employee_schedules")
    schedule: "Schedule" = Relationship(back_populates="employee_schedules")

class ScheduleChange(SQLModel, table=True):
    __tablename__ = "schedule_changes"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    schedule_id: int = Field(foreign_key="schedules.id")
    change_date: date
    change_time: time
    reason: ChangeReason
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    schedule: "Schedule" = Relationship(back_populates="schedule_changes")