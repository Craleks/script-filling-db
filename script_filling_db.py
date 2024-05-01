import pyodbc as db
import random

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
male_name = [
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
]
female_name = [
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
]


connection = db.connect(
    r"driver={ODBC Driver 17 for SQL Server}; server=DESKTOP-C8OR9VL\SQLEXPRESS; database=RegionalHospital; trusted_connection=yes"
)

cursor = connection.cursor()
cursor.execute(
    "select table_name from information_schema.tables where table_name NOT LIKE 'sys%'"
)
tables = [row.table_name for row in cursor.fetchall()]
# print(tables)

columns = {}
for table in tables:
    cursor.execute(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
    )
    columns[table] = [row.column_name for row in cursor.fetchall()]

# print(columns)


def random_fio(male_names, female_names, last_names, patronymics):
    fio = []
    for _ in range(300):
        chosen_last_name = random.choice(last_names)
        chosen_last_name = random.choice(last_names)
        chosen_patronymics = random.choice(patronymics)

        names = {"male": male_names, "female": female_names}
        gender = random.choice(list(names.keys()))
        chosen_name = random.choice(names[gender])

        if gender != "male":
            fio.append(f"{chosen_last_name}a {chosen_name} {chosen_patronymics[:-2]}на")
        else:
            fio.append(f"{chosen_last_name} {chosen_name} {chosen_patronymics}")
    print(fio)

    # print(f"{chosen_last_name}")

    # names = [male_name, female_name]
    # name_random = names[random.randint(0, 1)]
    # name = name_random[random.randint(0, len(name_random[random.randint(0, 1)]))]
    # name = random.randint(0, len(names[random.randint(0, 1)]))
    # last_name_index = random.choice(last_name)
    # print(f"{last_name_index}")


random_fio(male_name, female_name, last_name, patronymics)


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
