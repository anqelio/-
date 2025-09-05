def input_route_data()-> tuple[str, str, str, str, str, str, str]:
    """
    Коммуникация с пользователем. Заполнение информации о маршруте
    :return:
    """
    number = input("Номер маршрута: ")
    start_district = input("Начало маршрута: ")
    end_district = input("Конец маршрута: ")
    total_time_min = input("Общее время поездки: ")
    carrier_id = input("ID Перевозчика: ")
    operating_days = input("В какие дни ходит: ")
    transport_type_id = input("Тип транспорта: ")
    return number, start_district, end_district, total_time_min, carrier_id, operating_days, transport_type_id

def input_route_delete()-> str:
    """
    Коммуникация с пользователем. Заполнение информации о маршруте
    :return:
    """
    number = input("Номер маршрута, который вы хотите удалить: ")
    return number

def show_add_route_result(success: bool):
    """
    Вывод сообщения об операции добавления маршрута
    :param success:результат добавлния
    """
    if success:
        print("Маршрут успешно добавлен")
    else:
        print("Ошибка при добавлении маршрута")

def show_delete_route_result(success: bool):
    """
    Вывод сообщения об операции удаления маршрута
    :param success:результат удаления
    """
    if success:
        print("Маршрут успешно удален")
    else:
        print("Ошибка при удалении маршрута")

def show_routes(routes):
    """
    Вывод информации о всех клиентах (представление View)
    :param routes: список маршрутов
    :return:
    """
    print("Маршруты:")
    print(routes)
    for item in routes:
        print(f"Номер маршрута: {item[1]}, Начало маршрута: {item[2]}, Конец маршрута: {item[3]}, Общее время поездки: {item[4]}, ID Перевозчика: {item[5]}, В какие дни ходит: {item[6]}, Тип транспорта: {item[7]}")