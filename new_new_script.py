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
    "Specializations",
    "Doctors",
    "Patients",
    "Diseases",
    "Appointments",
    "FactTable",
]


def get_specialization_ids(cursor):
    cursor.execute("SELECT SpecializationID FROM Specializations")
    return [row.SpecializationID for row in cursor.fetchall()]


def get_address_ids(cursor):
    cursor.execute("SELECT AddressID FROM Addresses")
    return [row.AddressID for row in cursor.fetchall()]


def get_patient_ids(cursor):
    cursor.execute("SELECT PatientID FROM Patients")
    return [row.PatientID for row in cursor.fetchall()]


def get_doctor_ids(cursor):
    cursor.execute("SELECT DoctorID FROM Doctors")
    return [row.DoctorID for row in cursor.fetchall()]


def get_disease_ids(cursor):
    cursor.execute("SELECT DiseaseID FROM Diseases")
    return [row.DiseaseID for row in cursor.fetchall()]


def get_appointment_ids(cursor):
    cursor.execute("SELECT AppointmentID FROM Appointments")
    return [row.AppointmentID for row in cursor.fetchall()]


def generate_data():
    rd_gender = random.choice([Gender.MALE, Gender.FEMALE])
    specialization_ids = get_specialization_ids(cursor)
    address_ids = get_address_ids(cursor)
    patient_ids = get_patient_ids(cursor)
    doctor_ids = get_doctor_ids(cursor)
    disease_ids = get_disease_ids(cursor)
    appointment_ids = get_appointment_ids(cursor)
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
            "SpecializationID": random.choice(specialization_ids),
            "FIO": f"{person.last_name(gender=rd_gender)} {person.first_name(gender=rd_gender)} {ru.patronymic(gender=rd_gender)}",
            "PhoneNumber": person.phone_number(),
        },
        "Patients": {
            "AddressID": random.choice(address_ids),
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
            "PatientID": random.choice(patient_ids),
            "DoctorID": random.choice(doctor_ids),
            "AppointmentDate": person.birthdate(min_year=2018, max_year=2023),
        },
        "FactTable": {
            "PatientID": random.choice(patient_ids),
            "DiseaseID": random.choice(disease_ids),
            "DoctorID": random.choice(doctor_ids),
            "AppointmentID": random.choice(appointment_ids),
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


def get_primary_keys(cursor, table_name):
    cursor.execute(
        f"SELECT column_name FROM information_schema.key_column_usage WHERE OBJECTPROPERTY(OBJECT_ID(constraint_name), 'IsPrimaryKey') = 1 AND table_name = '{table_name}'"
    )
    primary_keys = [row.column_name for row in cursor.fetchall()]
    return primary_keys


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
        primary_keys = get_primary_keys(cursor, table)
        columns[table] = [
            column for column in columns[table] if column not in primary_keys
        ]
    return columns


def adding_data(columns, table_name, num_records):
    if table_name in columns:
        column_names = columns[table_name]
        clear_column_names = ", ".join(f"{name}" for name in column_names)

        for _ in range(num_records):
            data = generate_data()[table_name]

            values = ", ".join(f"'{value}'" for value in data.values())

            # print(f"INSERT INTO {table_name} ({clear_column_names}) VALUES ({values});")
            return f"INSERT INTO {table_name} ({clear_column_names}) VALUES ({values});"


connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=main_hospital; trusted_connection=yes"
)
cursor = connection.cursor()

tables = getting_table_names(cursor)
columns = getting_column_name(tables)

for table_name in table_filling_order:
    request_execution(cursor, adding_data(columns, table_name, 7))
