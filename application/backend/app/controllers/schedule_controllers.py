from sqlmodel import Session, select
from typing import List
from application.backend.app.models.transport_models import *
from datetime import time, date

class ScheduleController:
    def __init__(self, session: Session):
        self.session = session

    # Методы для расписания
    def create_schedule(self, route_id: int, departure_time: time, arrival_time: time) -> Schedule:
        schedule = Schedule(
            route_id=route_id,
            departure_time=departure_time,
            arrival_time=arrival_time
        )
        self.session.add(schedule)
        self.session.commit()
        self.session.refresh(schedule)
        return schedule

    def add_route_day(self, route_id: int, day_of_week: DaysOfWeek) -> RouteDay:
        route_day = RouteDay(route_id=route_id, day_of_week=day_of_week)
        self.session.add(route_day)
        self.session.commit()
        self.session.refresh(route_day)
        return route_day

    # Методы для сотрудников
    def create_employee(self, first_name: str, last_name: str, position: EmployeePosition,
                       hire_date: date, carrier_id: int) -> Employee:
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            position=position,
            hire_date=hire_date,
            carrier_id=carrier_id
        )
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def assign_employee_to_schedule(self, employee_id: int, schedule_id: int, work_date: date) -> EmployeeSchedule:
        employee_schedule = EmployeeSchedule(
            employee_id=employee_id,
            schedule_id=schedule_id,
            work_date=work_date
        )
        self.session.add(employee_schedule)
        self.session.commit()
        self.session.refresh(employee_schedule)
        return employee_schedule

    # Методы для изменений в расписании
    def log_schedule_change(self, schedule_id: int, change_date: date, change_time: time,
                           reason: ChangeReason, description: Optional[str] = None) -> ScheduleChange:
        change = ScheduleChange(
            schedule_id=schedule_id,
            change_date=change_date,
            change_time=change_time,
            reason=reason,
            description=description
        )
        self.session.add(change)
        self.session.commit()
        self.session.refresh(change)
        return change

    def get_all_employees(self) -> List[Employee]:
        statement = select(Employee)
        return self.session.exec(statement).all()