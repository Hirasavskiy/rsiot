import pyodbc


# Функция для установления соединения с базой данных
def create_connection():
    server = 'LENOVO-PC35\SQLEXPRESS'  # Имя сервера SQL Server
    database = 'lab1'  # Имя базы данных
    username = 'user'  # Имя пользователя
    password = '1234'  # Пароль
    driver = '{ODBC Driver 17 for SQL Server}'  # Драйвер для подключения к SQL Server
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    conn = pyodbc.connect(conn_str)

    # Проверяем наличие таблицы "vehicles"
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'vehicles'")
    if cursor.fetchone()[0] == 0:
        # Если таблица не существует, создаем её
        cursor.execute("""
            CREATE TABLE vehicles (
                id INT PRIMARY KEY IDENTITY,
                brand VARCHAR(255) NOT NULL,
                model VARCHAR(255) NOT NULL,
                year INT NOT NULL,
                license_plate VARCHAR(20) NOT NULL,
                vehicle_type VARCHAR(100) NOT NULL
            )
            """)
        conn.commit()

    return conn


# Функция для выполнения SQL-запросов с возвратом курсора (SELECT)
def execute_query(query, params=None):
    conn = create_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor




# Функция для выполнения SQL-запросов без возврата результатов (INSERT, UPDATE, DELETE)
def execute_non_query(query, params=None):
    conn = create_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()
