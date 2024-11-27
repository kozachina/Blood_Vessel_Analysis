import pymysql

# Параметри підключення
db_config = {
    "host": "localhost",
    "user": "root",  # Змініть на вашого користувача
    "password": "orbita1o",  # Вставте ваш пароль
    "database": "blood_vessel_diseases"  # Назва бази даних
}

# SQL-запити
create_database_query = "CREATE DATABASE IF NOT EXISTS BLOOD_VESSEL_DISEASES"
use_database_query = "USE BLOOD_VESSEL_DISEASES"
drop_table_query = "DROP TABLE IF EXISTS DISEASES"
create_table_query = """
CREATE TABLE DISEASES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    fractal_dimension_min DECIMAL(5, 2) NOT NULL,
    fractal_dimension_max DECIMAL(5, 2) NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""
insert_data_query = """
INSERT INTO DISEASES (disease_name, fractal_dimension_min, fractal_dimension_max) VALUES
    ('Норма', 1.85, 1.86),
    ('Аневризма', 1.87, 1.88),
    ('Тромбоз', 1.83, 1.84)
"""

try:
    # Підключення до MySQL
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Виконання SQL-запитів
    cursor.execute(create_database_query)
    cursor.execute(use_database_query)
    cursor.execute(drop_table_query)  # Видалення старої таблиці
    cursor.execute(create_table_query)
    cursor.execute(insert_data_query)

    # Фіксація змін
    connection.commit()
    print("База даних і таблиця створені успішно з діагнозами.")
except pymysql.MySQLError as e:
    print(f"Помилка: {e}")
finally:
    # Закриття з'єднання
    if connection:
        connection.close()
