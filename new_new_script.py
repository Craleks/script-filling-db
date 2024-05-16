import pyodbc as db
import random
from datetime import datetime as dt
from mimesis import Person, Address, Datetime
from mimesis.enums import Gender
from data import *

person = Person("ru")
address = Address("ru")
datetime = Datetime("ru")
disease_names = list(diseases.keys())
date_pattern = "%d.%m.%Y"
table_filling_order = [
    "Addresses",
    "Specializations",
    "Doctors",
    "Patients",
    "Diseases",
    "Appointments",
    "FactTable",
]


def generate_data():
    data = {
        "Addresses": {
            "AddressID": random.randint(1, 100),
            "Street": address.street_name(),
            "City": address.city(),
            "Districts": random.choice(districts),
        },
        "Specializations": {
            "SpecializationID": random.randint(1, 100),
            "SpecializationName": random.choice(names_specializations),
        },
        "Doctors": {
            "DoctorID": random.randint(1, 100),
            "SpecializationID": random.randint(1, 100),
            "FIO": person.full_name(),
            "PhoneNumber": person.telephone(),
        },
        "Patients": {
            "PatientID": random.randint(1, 100),
            "AddressID": random.randint(1, 100),
            "FIO": person.full_name(),
            "DateOfBirth": str(datetime.date(start=1950, end=2000)),
            "Gender": "M" if person.gender() == Gender.MALE else "F",
        },
        "Diseases": {
            "DiseaseID": random.randint(1, 100),
            "DiseaseName": random.choice(disease_names),
            "Symptoms": diseases[random.choice(disease_names)]["symptoms_diseases"],
            "Treatment": diseases[random.choice(disease_names)]["treatments_diseases"],
        },
        "Appointments": {
            "AppointmentID": random.randint(1, 100),
            "PatientID": random.randint(1, 100),
            "DoctorID": random.randint(1, 100),
            "AppointmentDate": "234",
        },
        "FactTable": {
            "FactID": random.randint(1, 100),
            "PatientID": random.randint(1, 100),
            "DiseaseID": random.randint(1, 100),
            "DoctorID": random.randint(1, 100),
            "AppointmentID": random.randint(1, 100),
        },
    }
    return data


def request_execution(cursor, request):
    try:
        cursor.execute(request)
        cursor.connection.commit()
        print("Запрос выполнен успешно")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


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
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
        )
        columns[table] = [row.column_name for row in cursor.fetchall()]
    return columns


def adding_data(columns, table_name, num_records):
    if table_name in columns:
        column_names = columns[table_name]
        clear_column_names = ", ".join(f"{name}" for name in column_names)

        for _ in range(num_records):
            data = generate_data()[table_name]

            values = ", ".join(f"'{value}'" for value in data.values())

            print(f"INSERT INTO {table_name} ({clear_column_names}) VALUES ({values});")
            # return f"INSERT INTO {table_name} ({clear_column_names}) VALUES ({values});"


connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=main_hospital; trusted_connection=yes"
)
cursor = connection.cursor()

tables = getting_table_names(cursor)
columns = getting_column_name(tables)

for table_name in table_filling_order:
    request_execution(cursor, adding_data(columns, table_name, 7))
