from app.db.database import create_db_and_tables, get_session
from app.controllers.transport_controllers import TransportController
from app.controllers.schedule_controllers import ScheduleController
from app.views.client_views import CLIViews
from app.models.transport_models import *
from datetime import time, date
from app.models.transport_models import TransportType, DaysOfWeek, EmployeePosition, ChangeReason
from application.backend.app.db.database import drop_tables

drop_tables()

def init_database():
    """Инициализация базы данных с тестовыми данными"""
    try:
        # Создание таблиц
        create_db_and_tables()
        print("Таблицы успешно созданы!")

        with next(get_session()) as session:
            transport_ctrl = TransportController(session)
            schedule_ctrl = ScheduleController(session)
            views = CLIViews()

            print("Создание тестовых данных...")

            # Создание перевозчиков
            carrier1 = transport_ctrl.create_carrier(
                name="ГорТранс",
                contact_phone="+7-123-456-7890",
                email="contact@gortrans.ru"
            )

            carrier2 = transport_ctrl.create_carrier(
                name="Автобусный парк №1",
                contact_phone="+7-123-456-7891"
            )

            # Создание остановок
            stop1 = transport_ctrl.create_stop("Центральная площадь", 55.7558, 37.6173, True)
            stop2 = transport_ctrl.create_stop("Железнодорожный вокзал", 55.7476, 37.6214, True)
            stop3 = transport_ctrl.create_stop("Улица Ленина", 55.7601, 37.6255, False)
            stop4 = transport_ctrl.create_stop("Парк Победы", 55.7368, 37.5166, True)

            # Создание маршрутов с типами транспорта
            route1 = transport_ctrl.create_route("101", TransportType.BUS, "Центральный", "Северный", 45, carrier1.id)
            route2 = transport_ctrl.create_route("23", TransportType.TRAM, "Западный", "Восточный", 30, carrier2.id)
            route3 = transport_ctrl.create_route("5", TransportType.TROLLEYBUS, "Южный", "Северный", 25, carrier1.id)

            # Добавление дней следования
            for day in [DaysOfWeek.MONDAY, DaysOfWeek.TUESDAY, DaysOfWeek.WEDNESDAY, DaysOfWeek.THURSDAY,
                        DaysOfWeek.FRIDAY]:
                schedule_ctrl.add_route_day(route1.id, day)

            for day in [DaysOfWeek.MONDAY, DaysOfWeek.WEDNESDAY, DaysOfWeek.FRIDAY, DaysOfWeek.SATURDAY,
                        DaysOfWeek.SUNDAY]:
                schedule_ctrl.add_route_day(route2.id, day)

            # Добавление остановок к маршрутам
            transport_ctrl.add_stop_to_route(route1.id, stop1.id, 1, time(8, 0))
            transport_ctrl.add_stop_to_route(route1.id, stop2.id, 2, time(8, 15))
            transport_ctrl.add_stop_to_route(route1.id, stop3.id, 3, time(8, 30))

            transport_ctrl.add_stop_to_route(route2.id, stop2.id, 1, time(9, 0))
            transport_ctrl.add_stop_to_route(route2.id, stop4.id, 2, time(9, 20))
            transport_ctrl.add_stop_to_route(route2.id, stop1.id, 3, time(9, 40))

            # Создание расписания
            schedule1 = schedule_ctrl.create_schedule(route1.id, time(8, 0), time(8, 45))
            schedule2 = schedule_ctrl.create_schedule(route1.id, time(10, 0), time(10, 45))
            schedule3 = schedule_ctrl.create_schedule(route2.id, time(9, 0), time(9, 40))

            # Создание сотрудников
            driver1 = schedule_ctrl.create_employee(
                "Иван", "Петров", EmployeePosition.DRIVER,
                date(2020, 1, 15), carrier1.id
            )

            conductor1 = schedule_ctrl.create_employee(
                "Мария", "Сидорова", EmployeePosition.CONDUCTOR,
                date(2021, 3, 20), carrier1.id
            )

            driver2 = schedule_ctrl.create_employee(
                "Алексей", "Козлов", EmployeePosition.DRIVER,
                date(2019, 5, 10), carrier2.id
            )

            # Назначение сотрудников на рейсы
            schedule_ctrl.assign_employee_to_schedule(driver1.id, schedule1.id, date(2024, 1, 15))
            schedule_ctrl.assign_employee_to_schedule(conductor1.id, schedule1.id, date(2024, 1, 15))
            schedule_ctrl.assign_employee_to_schedule(driver2.id, schedule3.id, date(2024, 1, 15))

            # Логирование изменения расписания
            schedule_ctrl.log_schedule_change(
                schedule1.id, date(2024, 1, 15), time(8, 5),
                ChangeReason.WEATHER, "Задержка из-за снегопада"
            )

            # Отображение данных
            print("\n" + "=" * 50)
            stops = transport_ctrl.get_all_stops()
            views.display_stops(stops)

            print("\n" + "=" * 50)
            routes = transport_ctrl.get_all_routes()
            views.display_routes(routes)

            print("\n" + "=" * 50)
            route_stops = transport_ctrl.get_route_stops(route1.id)
            views.display_route_stops(route_stops)

            print("\n" + "=" * 50)
            employees = schedule_ctrl.get_all_employees()
            views.display_employees(employees)

            print("\n" + "=" * 50)
            print("Тестовые данные успешно созданы!")

    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")

if __name__ == "__main__":
    init_database()