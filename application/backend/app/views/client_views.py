from typing import List
from application.backend.app.models.transport_models import *

class CLIViews:
    @staticmethod
    def display_stops(stops: List[Stop]):
        print("\n=== ОСТАНОВКИ ===")
        for stop in stops:
            pavilion = "Есть" if stop.has_pavilion else "Нет"
            print(f"{stop.id}: {stop.name} ({stop.latitude}, {stop.longitude}) Павильон: {pavilion}")

    @staticmethod
    def display_routes(routes: List[Route]):
        print("\n=== МАРШРУТЫ ===")
        for route in routes:
            print(f"{route.route_number}: {route.start_district} -> {route.end_district} "
                  f"({route.total_travel_time} мин)")

    @staticmethod
    def display_route_stops(route_stops: List[RouteStop]):
        print("\n=== ОСТАНОВКИ МАРШРУТА ===")
        for rs in route_stops:
            print(f"{rs.stop_order}. {rs.stop.name} - {rs.arrival_time}")

    @staticmethod
    def display_employees(employees: List[Employee]):
        print("\n=== СОТРУДНИКИ ===")
        for emp in employees:
            print(f"{emp.first_name} {emp.last_name} - {emp.position.value}")

    @staticmethod
    def display_schedule_changes(changes: List[ScheduleChange]):
        print("\n=== ИЗМЕНЕНИЯ РАСПИСАНИЯ ===")
        for change in changes:
            print(f"{change.change_date} {change.change_time}: {change.reason.value} - {change.description}")