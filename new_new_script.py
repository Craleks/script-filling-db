import pyodbc as db
import random
from data import *
from mimesis import Address
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider

address = Address("ru")

table_filling_order = [
    "Addresses",
    # "Specializations",
    # "Doctors",
    # "Patients",
    # "Diseases",
    # "Appointments",
    # "FactTable",
]

def generate_data():
    street_name = "ул. " + address.street_name()
    house_number = str(random.randint(1, 200))
    apartment_number = "кв. " + str(random.randint(1, 200))
    full_address = f"{street_name} {house_number}, {apartment_number}"

    data = {
        "Addresses": {
            "Street": full_address,
            "City": address.city(),
            "Districts": random.choice(districts),
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
    cursor.execute(f"SELECT column_name FROM information_schema.key_column_usage WHERE OBJECTPROPERTY(OBJECT_ID(constraint_name), 'IsPrimaryKey') = 1 AND table_name = '{table_name}'")
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
        columns[table] = [column for column in columns[table] if column not in primary_keys]
    return columns

def adding_data(columns, table_name, num_records):
    if table_name in columns:
        column_names = columns[table_name]
        clear_column_names = ", ".join(f"{name}" for name in column_names)

        for _ in range(num_records):
            data = generate_data()[table_name]

            values = ", ".join(f"'{value}'" for value in data.values())

            print(f"INSERT INTO {table_name} ({clear_column_names}) VALUES ({values});")
            return f"INSERT INTO {table_name} ({clear_column_names}) VALUES ({values});"

connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=main_hospital; trusted_connection=yes"
)
cursor = connection.cursor()

tables = getting_table_names(cursor)
columns = getting_column_name(tables)

for table_name in table_filling_order:
    request_execution(cursor, adding_data(columns, table_name, 7))
