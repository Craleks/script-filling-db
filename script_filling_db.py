import pyodbc as db
import random
from data import *

"""
TODO:
1. Сделать рандомное создание "Адрес", где будет улица, город и район
2. Сделать рандомное создание "Пациент", где будет:
    - рандомно созданное "ФИО" +
    - рандомно созданное "дата рождения" +
    - присваивание пола отталкиваясь от "ФИО" +

{'Addresses': ['AddressID', 'Street', 'City', 'Region'], 
'Appointments': ['AppointmentID', 'PatientID', 'DoctorID', 'AppointmentDate'],
'Diseases': ['DiseaseID', 'DiseaseName', 'Symptoms', 'Treatment'],
'Doctors': ['DoctorID', 'FIO', 'SpecializationID', 'PhoneNumber'],
'FactTable': ['FactID', 'PatientID', 'DiseaseID', 'DoctorID', 'AppointmentID'],
'Patients': ['PatientID', 'FIO', 'DateOfBirth', 'Gender', 'AddressID'],
'Specializations': ['SpecializationID', 'SpecializationName']}

use [RegionalHospital]
--SELECT table_name FROM information_schema.tables

--SELECT * FROM Addresses
select table_name from information_schema.tables where table_name NOT LIKE 'sys%'
"""


def random_fio():
    fio = []
    for _ in range(300):
        chosen_last_name = random.choice(last_names)
        chosen_last_name = random.choice(last_names)
        chosen_patronymics = random.choice(patronymics)

        gender = random.choice(list(names.keys()))
        chosen_name = random.choice(names[gender])

        if gender != "male":
            fio.append(
                f"{gender} - {chosen_last_name}a {chosen_name} {chosen_patronymics[:-2]}на"
            )
        else:
            fio.append(
                f"{gender} - {chosen_last_name} {chosen_name} {chosen_patronymics}"
            )
    return fio


def random_birthday():
    year = random.randint(1950, 2010)
    month = random.randint(1, 12)

    if month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:
        day = random.randint(1, 31)
    return f"{day}.{month}.{year}"


def random_address(count):
    for _ in range(count):
        city = random.choice(cities)
        street = random.choice(streets)
        district = random.choice(districts)
        house_number = random.randint(1, 127)
        apartment_number = random.randint(1, 99)

        return f'"ул. {street}, дом {house_number}, кв. {apartment_number}", "{city}", "{district}"'


# # cursor = connection.cursor()
# # cursor.execute(
# #     "select table_name from information_schema.tables where table_name NOT LIKE 'sys%'"
# # )
# # tables = [row.table_name for row in cursor.fetchall()]

# columns = {}
# for table in tables:
#     cursor.execute(
#         f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' AND column_name NOT LIKE '%ID%'"
#     )
#     columns[table] = [row.column_name for row in cursor.fetchall()]
#     # cursor.execute(f"INSERT INTO {table} (AddressID, Street, City, Region) VALUES ")

# for key, column_names in columns.items():
#     clear_column_names = ", ".join(f"{name}" for name in column_names)
#     print(f"INSERT INTO {key} ({clear_column_names})")


# def add_data():
#     for key, column_names in columns.items():
#     clear_column_names = ", ".join(f"{name}" for name in column_names)
#     print(f"INSERT INTO {key} ({clear_column_names})")


def getting_table_names(connection, cursor):
    cursor.execute(
        "select table_name from information_schema.tables where table_name NOT LIKE 'sys%'"
    )
    tables = [row.table_name for row in cursor.fetchall()]
    return tables


def getting_column_name(tables):
    columns = {}
    for table in tables:
        cursor.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' AND column_name NOT LIKE '%ID%'"
        )
        columns[table] = [row.column_name for row in cursor.fetchall()]
    return columns


def adding_data(columns, table_name):
    if table_name in columns:
        column_names = columns[table_name]
        clear_column_names = ", ".join(f"{name}" for name in column_names)
        print(f"INSERT INTO {table_name} ({clear_column_names}) VALUES ()")
    else:
        print(f"Таблица {table_name} не найдена.")


connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=RegionalHospital; trusted_connection=yes"
)
cursor = connection.cursor()

tables = getting_table_names(connection, cursor)
columns = getting_column_name(tables)

for i, name in enumerate(tables, start=1):
    print(f"{i} - {name}")
name_table = int(input("Введите номер таблицы которую хотите заполнить: "))

adding_data(columns, tables[name_table - 1])
