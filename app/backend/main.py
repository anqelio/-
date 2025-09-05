from db.database import init_db
from app.backend.views.routes_view import input_route_data, show_add_route_result, input_route_delete, \
    show_delete_route_result, input_route_update, show_update_route_result
from app.backend.controllers import routes_controller
from app.backend.views.routes_view import show_routes

def main():
    init_db()
    while True:
        print("\nМеню:")
        print("1. Добавить новый маршрут")
        print("2. Удалить маршрут")
        print("3. Изменить маршрут")
        print("4. Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            number, start_district, end_district, total_time_min, carrier_id, operating_days, transport_type_id = input_route_data()
            success = routes_controller.add_route(number, start_district, end_district, total_time_min, carrier_id,operating_days, transport_type_id)
            show_add_route_result(success)
        if choice == '2':
            number = input_route_delete()
            success = routes_controller.delete_route(number)
            show_delete_route_result(success)
        elif choice == "3":
            list_arr = routes_controller.get_list_routes()
            show_routes(list_arr)
        elif choice == "4":
            print("Выход")
            break
        else:
            print("Неверный выбор")
if __name__ == "__main__":
    main()
