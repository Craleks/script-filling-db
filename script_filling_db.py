import pyodbc as db
import random
from datetime import datetime
from data import *

"""
ПОРЯДОК ЗАПОЛНЕНИЯ ТАБЛИЦ
1. Addresses: Эта таблица не имеет зависимостей от других таблиц, поэтому её можно заполнить первой.
2. Specializations: Эта таблица также не имеет зависимостей от других таблиц, поэтому её можно заполнить после таблицы Addresses.
3. Doctors: Эта таблица зависит от таблицы Specializations, поэтому её следует заполнить после таблицы Specializations.
4. Patients: Эта таблица зависит от таблицы Addresses, поэтому её следует заполнить после таблицы Addresses.
5. Diseases: Эта таблица не имеет зависимостей от других таблиц, поэтому её можно заполнить после предыдущих таблиц.
6. Appointments: Эта таблица зависит от таблиц Doctors и Patients, поэтому её следует заполнить после этих таблиц.
7. FactTable: Эта таблица зависит от всех остальных таблиц, поэтому её следует заполнить последней.


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

table_filling_order = [
    "Addresses",
    "Specializations",
    "Doctors",
    "Patients",
    "Diseases",
    "Appointments",
]


def generate_phone_number(count):
    phone_numbers = []
    for _ in range(count):
        number = "".join(random.choice("0123456789") for _ in range(10))
        phone_numbers.append(f"'{number}'")

    return phone_numbers


def choose_random_disease(count):
    diseases_info = []
    for _ in range(count):
        disease = random.choice(list(diseases.keys()))
        symptoms = diseases[disease]["symptoms_diseases"]
        treatment = diseases[disease]["treatments_diseases"]
        diseases_info.append((disease, symptoms, treatment))

    return diseases_info


def fio_random(count):
    fio = []
    genders = []
    for _ in range(count):
        chosen_last_name = random.choice(last_names)
        chosen_patronymics = random.choice(patronymics)

        gender = random.choice(list(names.keys()))
        chosen_name = random.choice(names[gender])

        if gender != "male":
            fio.append(
                f"'{chosen_last_name}a {chosen_name} {chosen_patronymics[:-2]}на'"
            )
            genders.append('Ж')
        else:
            fio.append(f"'{chosen_last_name} {chosen_name} {chosen_patronymics}'")
            genders.append('М')
    return fio, genders


def random_date(count):
    dates = []
    for _ in range(count):
        year = random.randint(2017, datetime.now().year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        dates.append(f"{day}.{month}.{year}")
    return dates


def birthday_random(count):
    dates = []
    for _ in range(count):
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

        dates.append(f"{day}.{month}.{year}")
    return dates


def address_random(count):
    addresses = []
    for _ in range(count):
        city = random.choice(cities)
        street = random.choice(streets)
        district = random.choice(districts)
        house_number = random.randint(1, 127)
        apartment_number = random.randint(1, 99)

        address = f"'ул. {street}, дом {house_number}, кв. {apartment_number}', '{city}', '{district}'"
        addresses.append(address)

    return addresses


def specializations_random(count):
    specializations = []
    for _ in range(count):
        specialization = random.choice(names_specializations)
        specializations.append(f"'{specialization}'")

    return specializations


def getting_table_names(cursor):
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

        match table_name:
            case "Addresses":
                values = ", ".join(f"({address})" for address in address_random(10))
            case "Specializations":
                values = ", ".join(
                    f'({specialization})'
                    for specialization in specializations_random(2)
                )
            case "Doctors":
                fio, genders = fio_random(3)
                values = ", ".join(
                    f"({fio}, {phone_number})"
                    for fio, phone_number in zip(fio, generate_phone_number(3))
                )
            case "Patients":
                fio, genders = fio_random(3)
                values = ", ".join(
                    f"({fio}, '{birthday}', '{gender}')"
                    for fio, birthday, gender in zip(
                        fio, birthday_random(3), genders
                    )
                )
            case "Diseases":
                diseases_info = choose_random_disease(14)
                values = ", ".join(
                    f"('{disease}', '{symptom}', '{treatment}')"
                    for disease, symptom, treatment in diseases_info
                )
            case "Appointments":
                values = ", ".join(f"('{date}')" for date in random_date(10))
        return f"INSERT INTO {table_name} ({clear_column_names}) VALUES {values};"


def request_execution(cursor, request):
    try:
        cursor.execute(request)
        cursor.connection.commit()  # сохраняем изменения
        print("Запрос выполнен успешно")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=hosp_test1; trusted_connection=yes"
)
cursor = connection.cursor()

tables = getting_table_names(cursor)
columns = getting_column_name(tables)

for table_name in table_filling_order:
    request_execution(cursor, adding_data(columns, table_name))
