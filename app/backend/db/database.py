import sqlite3

def init_db():
    '''
    Инициализация базы данных transport.db
    :return:
    '''

    try:
        conn = sqlite3.connect("transport.db")
        cursor = conn.cursor()
        # Проверяем подключение
        cursor.execute("SELECT 1")
        cursor.executescript('''
        -- 1. Таблица видов транспорта
        CREATE TABLE IF NOT EXISTS transport_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        
        -- 2 Таблица остановок
        CREATE TABLE IF NOT EXISTS stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            has_pavilion BOOLEAN NOT NULL DEFAULT 0
        );
        
        -- 3 Таблица перевозчиков
        CREATE TABLE IF NOT EXISTS carriers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            contact_info TEXT
        );
        
        -- 4 Таблица маршрутов
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            start_district TEXT NOT NULL,
            end_district TEXT NOT NULL,
            total_time_min INTEGER NOT NULL,
            carrier_id INTEGER NOT NULL,
            operating_days TEXT NOT NULL,
            transport_type_id INTEGER NOT NULL,
            FOREIGN KEY (carrier_id) REFERENCES carriers(id),
            FOREIGN KEY (transport_type_id) REFERENCES transport_types(id)
        );
        
        -- 5 Таблица связи маршрутов и остановок
        CREATE TABLE IF NOT EXISTS route_stops (
            route_id INTEGER,
            stop_id INTEGER,
            stop_order INTEGER NOT NULL,
            PRIMARY KEY (route_id, stop_id),
            FOREIGN KEY (route_id) REFERENCES routes(id),
            FOREIGN KEY (stop_id) REFERENCES stops(id)
        );
        
        -- 6 Таблица сотрудников
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL CHECK (position IN ('водитель', 'кондуктор')),
            carrier_id INTEGER NOT NULL,
            FOREIGN KEY (carrier_id) REFERENCES carriers(id)
        );
        
        -- 7 Таблица рейсов
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_id INTEGER NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            FOREIGN KEY (route_id) REFERENCES routes(id)
        );
        
        -- 8 Таблица выхода сотрудников на маршруты
        CREATE TABLE IF NOT EXISTS employee_trip (
            employee_id INTEGER,
            trip_id INTEGER,
            PRIMARY KEY (employee_id, trip_id),
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (trip_id) REFERENCES trips(id)
        );
        
        -- 9 Таблица изменений расписания
        CREATE TABLE IF NOT EXISTS schedule_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            change_date DATE NOT NULL,
            change_time TIME NOT NULL,
            reason TEXT NOT NULL,
            new_start_time TIME,
            new_end_time TIME,
            FOREIGN KEY (trip_id) REFERENCES trips(id)
        );
        ''')
        conn.commit()
        print("База данных инициализирована успешно!")
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Ошибка инициализации базы данных: {e}")
        return None, None

conn, cursor = init_db()
if conn and cursor:
    print("Можно продолжать работу")
else:
    print("Не удалось подключиться к базе данных")