from app.backend.db.database import conn, cursor

def add_route(number, start_district, end_district, total_time_min, carrier_id, operating_days, transport_type_id)-> bool:
    """
    Добавление маршрута
    :param number: номер маршрута
    :param start_district: начало маршрута
    :param end_district: конец маршрута
    :param total_time_min: общее время в пути
    :param carrier_id: ID перевозчика
    :param operating_days: в какие дни ходит
    :param transport_type_id: тип транспорта
    :return: True, если добавление успешно, иначе False
    """
    try:
        cursor.execute("INSERT INTO routes (number, start_district, end_district, total_time_min, carrier_id, operating_days, transport_type_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (number, start_district, end_district, total_time_min, carrier_id, operating_days, transport_type_id))
        conn.commit()
        return True
    except Exception:
        return False

def delete_route(number)-> bool:
    """
    Добавление маршрута
    :param id: ID маршрута
    :return: True, если добавление успешно, иначе False
    """
    cursor.execute("DELETE FROM routes WHERE number = ?", (number,))
    conn.commit()
    return True

def get_list_routes()->list[tuple]:
    """
    Вывод информации о всех клиентах
    :return: массив из кортежей с информацией о маршрутах
    """
    cursor.execute("SELECT * FROM routes")
    return cursor.fetchall()