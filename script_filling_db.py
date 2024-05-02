import pyodbc as db
import random

"""
TODO:
1. Сделать рандомное создание "Адрес", где будет улица, город и район
2. Сделать рандомное создание "Пациент", где будет:
    - рандомно созданное "ФИО" +
    - рандомно созданное "дата рождения"
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

#!fio
last_name = [
    "Иванов",
    "Смирнов",
    "Кузнецов",
    "Попов",
    "Васильев",
    "Петров",
    "Соколов",
    "Михайлов",
    "Новиков",
    "Федоров",
    "Морозов",
    "Волков",
    "Алексеев",
    "Лебедев",
    "Семенов",
    "Егоров",
    "Павлов",
    "Козлов",
    "Степанов",
    "Николаев",
]
patronymics = [
    "Александрович",
    "Максимович",
    "Иванович",
    "Артемович",
    "Дмитриевич",
    "Никитович",
    "Михайлович",
    "Егорович",
    "Ильич",
    "Даниилович",
    "Романович",
    "Сергеевич",
    "Владимирович",
    "Андреевич",
    "Алексеевич",
    "Денисович",
    "Кириллович",
    "Олегович",
    "Степанович",
    "Ярославович",
]
names = {
    "male": [
        "Александр",
        "Максим",
        "Иван",
        "Артем",
        "Дмитрий",
        "Никита",
        "Михаил",
        "Егор",
        "Илья",
        "Даниил",
        "Роман",
        "Сергей",
        "Владимир",
        "Андрей",
        "Алексей",
        "Денис",
        "Кирилл",
        "Олег",
        "Степан",
        "Ярослав",
    ],
    "female": [
        "Анастасия",
        "Анна",
        "Виктория",
        "Мария",
        "Ирина",
        "Юлия",
        "Ольга",
        "Татьяна",
        "Екатерина",
        "Полина",
        "Елена",
        "Дарья",
        "Ксения",
        "Александра",
        "Евгения",
        "Светлана",
        "Алина",
        "Елизавета",
        "Наталья",
        "Валерия",
    ],
}

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
        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
    )
    columns[table] = [row.column_name for row in cursor.fetchall()]
# print(columns)


def random_fio(names, last_names, patronymics):
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
    print(fio)


random_fio(names, last_name, patronymics)


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
