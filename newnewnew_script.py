import pyodbc as db
import random
from data import *
from mimesis import Address, Person
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider

address = Address("ru")
person = Person("ru")
ru = RussiaSpecProvider()
disease_names = list(diseases.keys())

table_filling_order = [
    "Addresses",
    "Doctors",
    "Patients",
    "Appointments",
    "FactTable",
]


def get_primary_keys(cursor, table_name):
    cursor.execute(
        f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_NAME = '{table_name}' AND
        OBJECTPROPERTY(OBJECT_ID(CONSTRAINT_SCHEMA + '.' + CONSTRAINT_NAME), 'IsPrimaryKey') = 1
    """
    )
    return [row[0] for row in cursor.fetchall()]


def get_ids(cursor, column_name, table_name):
    cursor.execute(f"SELECT {column_name} FROM {table_name}")
    return [row[0] for row in cursor.fetchall()]


def request_execution(cursor, requests):
    for request in requests:
        try:
            cursor.execute(request)
            cursor.connection.commit()
            print("Запрос выполнен успешно")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def generate_addresses_data():
    return {
        "Street": f"ул. {address.street_name()} {random.randint(1, 200)}, кв. {random.randint(1, 200)}",
        "City": address.city(),
        "Districts": random.choice(districts),
    }


def generate_specializations_data():
    return {
        "SpecializationName": random.choice(names_specializations),
    }


def generate_doctors_data():
    rd_gender = random.choice([Gender.MALE, Gender.FEMALE])
    return {
        "SpecializationID": random.choice(
            get_ids(cursor, "SpecializationID", "Specializations")
        ),
        "FIO": f"{person.last_name(gender=rd_gender)} {person.first_name(gender=rd_gender)} {ru.patronymic(gender=rd_gender)}",
        "PhoneNumber": person.phone_number(),
    }


def generate_patients_data():
    rd_gender = random.choice([Gender.MALE, Gender.FEMALE])
    return {
        "AddressID": random.choice(get_ids(cursor, "AddressID", "Addresses")),
        "FIO": f"{person.last_name(gender=rd_gender)} {person.first_name(gender=rd_gender)} {ru.patronymic(gender=rd_gender)}",
        "DateOfBirth": person.birthdate(min_year=1980, max_year=2023),
        "Gender": str(rd_gender.name)[0],
    }


def generate_diseases_data():
    disease_name = random.choice(disease_names)
    return {
        "DiseaseName": disease_name,
        "Symptoms": diseases[disease_name]["symptoms_diseases"],
        "Treatment": diseases[disease_name]["treatments_diseases"],
    }


def generate_appointments_data():
    return {
        "PatientID": random.choice(get_ids(cursor, "PatientID", "Patients")),
        "DoctorID": random.choice(get_ids(cursor, "DoctorID", "Doctors")),
        "AppointmentDate": person.birthdate(min_year=2018, max_year=2023),
    }


def generate_fact_table_data():
    return {
        "PatientID": random.choice(get_ids(cursor, "PatientID", "Patients")),
        "DiseaseID": random.choice(get_ids(cursor, "DiseaseID", "Diseases")),
        "DoctorID": random.choice(get_ids(cursor, "DoctorID", "Doctors")),
        "AppointmentID": random.choice(
            get_ids(cursor, "AppointmentID", "Appointments")
        ),
    }


def generate_data_for_table(table_name):
    match table_name:
        case "Addresses":
            return generate_addresses_data()
        case "Specializations":
            return generate_specializations_data()
        case "Doctors":
            return generate_doctors_data()
        case "Patients":
            return generate_patients_data()
        case "Diseases":
            return generate_diseases_data()
        case "Appointments":
            return generate_appointments_data()
        case "FactTable":
            return generate_fact_table_data()


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


def adding_data(table_name, num_records, columns):
    primary_keys = get_primary_keys(cursor, table_name)
    clear_column_names = [
        name for name in columns[table_name] if name not in primary_keys
    ]
    clear_column_names_str = ", ".join(clear_column_names)

    requests = []

    for _ in range(num_records):
        data = generate_data_for_table(table_name)
        values = ", ".join(f"'{value}'" for key, value in data.items())
        request = (
            f"INSERT INTO {table_name} ({clear_column_names_str}) VALUES ({values});"
        )
        requests.append(request)
    return requests


connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=main_hospital; trusted_connection=yes"
)

with connection.cursor() as cursor:
    tables = getting_table_names(cursor)
    columns = getting_column_name(tables)

    for table_name in table_filling_order:
        requests = adding_data(table_name, 100, columns)
        request_execution(cursor, requests)
