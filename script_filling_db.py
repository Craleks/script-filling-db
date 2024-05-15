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


connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=RegionalHospital; trusted_connection=yes"
)

cursor = connection.cursor()
cursor.execute(
    "select table_name from information_schema.tables where table_name NOT LIKE 'sys%'"
)
tables = [row.table_name for row in cursor.fetchall()]

columns = {}
for table in tables:
    cursor.execute(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' AND column_name NOT LIKE '%ID%'"
    )
    columns[table] = [row.column_name for row in cursor.fetchall()]
    # cursor.execute(f"INSERT INTO {table} (AddressID, Street, City, Region) VALUES ")

for key, column_names in columns.items():
    clear_column_names = ", ".join(f"{name}" for name in column_names)
    print(f"INSERT INTO {key} ({clear_column_names})")


# for table in table
# print(columns)


# def random_fio(names, last_names, patronymics):
#     fio = []
#     for _ in range(300):
#         chosen_last_name = random.choice(last_names)
#         chosen_last_name = random.choice(last_names)
#         chosen_patronymics = random.choice(patronymics)

#         gender = random.choice(list(names.keys()))
#         chosen_name = random.choice(names[gender])

#         if gender != "male":
#             fio.append(
#                 f"{gender} - {chosen_last_name}a {chosen_name} {chosen_patronymics[:-2]}на"
#             )
#         else:
#             fio.append(
#                 f"{gender} - {chosen_last_name} {chosen_name} {chosen_patronymics}"
#             )

#     return fio


# def random_birthday():
#     year = random.randint(1950, 2010)
#     month = random.randint(1, 12)

#     if month == 2:
#         if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
#             day = random.randint(1, 29)
#         else:
#             day = random.randint(1, 28)
#     elif month in [4, 6, 9, 11]:
#         day = random.randint(1, 30)
#     else:
#         day = random.randint(1, 31)

#     return f"{day}.{month}.{year}"


# def random_address(cities, streets, districts):
#     for _ in range(100):
#         city = random.choice(cities)
#         street = random.choice(streets)
#         district = random.choice(districts)
#         house_number = random.randint(1, 127)
#         apartment_number = random.randint(1, 99)

#         print(
#             f"Город {city}, {district} район, ул. {street}, дом {house_number}, кв. {apartment_number}"
#         )


# for key, values in columns.items():
#     for value in values:
#         print(f"Ключ: {key}, Значение: {value}")
# for name_column in tab:
# print()

# for tab in tables:
# for name_column in tab:
# print(name_column)
# print(columns[tab])

# random_address(cities, streets, districts)
# print(address)
# fio = random_fio(names, last_name, patronymics)
# print(fio)
# date_of_birth = random_birthday()
# print(date_of_birth)


# with connection as conn:
#     cursor = conn.cursor()
#     cursor.execute(
#         "select table_name from information_schema.tables where table_name NOT LIKE 'sys%'"
#     )

#     cursor.execute(
#         "SELECT column_name FROM information_schema.columns WHERE table_name = 'your_table_name'"
#     )

#     # rows = cursor.fetchall()

#     while True:
#         rows = cursor.fetchone()
#         if not rows:
#             break
#         for row in rows:
#             name_tables.append(row)
#     print(name_tables)

# # cursor = conn.cursor()
# # cursor.execute("SELECT table_name FROM information_schema.tables")
# # while 1:
# #     row = cursor.fetchone()
# #     if not row:
# #         break
# #     print(row.table_name)
# # conn.close()


# while 1:
#     rows = cursor.fetchone()
#     for row in rows:
#         if not row:
#             break
#         name_tables.append(row)

# print(name_tables)

# print(rows)
# cursor.execute("insert")
# for row in rows:
#     print(row)


# import pyodbc

# connection = pyodbc.connect(
#     r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=RegionalHospital; trusted_connection=yes"
# )


# with conn as connection:
#     # Создайте курсор
#     cursor = conn.cursor()

#     # Выполните SQL-запрос
#     cursor.execute(
#         "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_catalog='your_database_name'"
#     )

#     # Получите результаты
#     rows = cursor.fetchall()

#     # Выведите результаты
#     for row in rows:
#         print(row)


# # cursor = conn.cursor()
# # cursor.execute("SELECT table_name FROM information_schema.tables")
# # rows = cursor.fetchall()

# # for row in rows:
# #     print(row)

# # with connection.cursor() as cursor:
# # rows = cursor.fetchall()

# # cursor = conn.cursor()
# # cursor.execute("SELECT table_name FROM information_schema.tables")
# # while 1:
# #     row = cursor.fetchone()
# #     if not row:
# #         break
# #     print(row.table_name)
# # conn.close()
