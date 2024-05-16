import pyodbc as db
import random
from data import *
from mimesis import Address, Person
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider
import logging

# Настройка логирования
logging.basicConfig(filename="database.log", level=logging.ERROR)

address = Address("ru")
person = Person("ru")
ru = RussiaSpecProvider()
disease_names = list(diseases.keys())

table_filling_order = [
    "Addresses",
    "Specializations",
    "Doctors",
    "Patients",
    "Diseases",
    "Appointments",
    "FactTable",
]


def get_ids(cursor, column_name, table_name):
    cursor.execute(f"SELECT {column_name} FROM {table_name}")
    return [row[0] for row in cursor.fetchall()]


def request_execution(cursor, request):
    try:
        cursor.execute(request)
        cursor.connection.commit()
        print("Запрос выполнен успешно")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


def generate_data():
    rd_gender = random.choice([Gender.MALE, Gender.FEMALE])
    data = {
        "Addresses": {
            "Street": f"ул. {address.street_name()} {random.randint(1, 200)}, кв. {random.randint(1, 200)}",
            "City": address.city(),
            "Districts": random.choice(districts),
        },
        "Specializations": {
            "SpecializationName": random.choice(names_specializations),
        },
        "Doctors": {
            "SpecializationID": random.choice(
                get_ids(cursor, "SpecializationID", "Specializations")
            ),
            "FIO": f"{person.last_name(gender=rd_gender)} {person.first_name(gender=rd_gender)} {ru.patronymic(gender=rd_gender)}",
            "PhoneNumber": person.phone_number(),
        },
        "Patients": {
            "AddressID": random.choice(get_ids(cursor, "AddressID", "Addresses")),
            "FIO": f"{person.last_name(gender=rd_gender)} {person.first_name(gender=rd_gender)} {ru.patronymic(gender=rd_gender)}",
            "DateOfBirth": person.birthdate(min_year=1980, max_year=2023),
            "Gender": str(rd_gender.name)[0],
        },
        "Diseases": {
            "DiseaseName": random.choice(disease_names),
            "Symptoms": diseases[random.choice(disease_names)]["symptoms_diseases"],
            "Treatment": diseases[random.choice(disease_names)]["treatments_diseases"],
        },
        "Appointments": {
            "PatientID": random.choice(get_ids(cursor, "PatientID", "Patients")),
            "DoctorID": random.choice(get_ids(cursor, "DoctorID", "Doctors")),
            "AppointmentDate": person.birthdate(min_year=2018, max_year=2023),
        },
        "FactTable": {
            "PatientID": random.choice(get_ids(cursor, "PatientID", "Patients")),
            "DiseaseID": random.choice(get_ids(cursor, "DiseaseID", "Diseases")),
            "DoctorID": random.choice(get_ids(cursor, "DoctorID", "Doctors")),
            "AppointmentID": random.choice(
                get_ids(cursor, "AppointmentID", "Appointments")
            ),
        },
    }
    return data


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


def adding_data(table_name, num_records):
    columns = getting_column_name(table_name)
    clear_column_names = ", ".join(f"{name}" for name in columns)

    for _ in range(num_records):
        data = generate_data()[table_name]

        values = ", ".join(f"'{value}'" for value in data.values())

        print(f"INSERT INTO {table_name} ({clear_column_names}) VALUES ({values});")
        return f"INSERT INTO {table_name} ({clear_column_names}) VALUES ({values});"


connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=main_hospital; trusted_connection=yes"
)

with connection.cursor() as cursor:
    tables = getting_table_names(cursor)
    columns = getting_column_name(tables)
    for table_name in table_filling_order:
        request_execution(cursor, adding_data(table_name, 7))
