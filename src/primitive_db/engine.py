import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import create_table, delete, drop_table, insert, select, update
from primitive_db.parser import parse_set, parse_values, parse_where
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def welcome():
    print("Первая попытка запустить проект!")
    print()
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    command = prompt.string("Введите команду: ")
    while command != "exit":
        if command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        command = prompt.string("Введите команду: ")


def print_help():
    """Prints the help message for the current mode."""
    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
        "where <столбец_условия> = <значение_условия> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help- справочная информация\n")


def show_table(metadata, table_name, rows):
    columns = []
    for column in metadata[table_name]:
        name = column.split(":")[0]
        columns.append(name)

    table = PrettyTable()
    table.field_names = columns
    for row in rows:
        line = []
        for name in columns:
            line.append(row[name])
        table.add_row(line)
    print(table)


def run():
    print_help()
    while True:
        metadata = load_metadata("db_meta.json")
        user_input = input("Введите команду: ")
        args = shlex.split(user_input)
        if len(args) == 0:
            continue
        command = args[0]

        if command == "exit":
            break
        elif command == "help":
            print_help()
        elif command == "list_tables":
            for table_name in metadata:
                print(f"- {table_name}")
        elif command == "create_table":
            if len(args) < 3:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[1]
            columns = args[2:]
            existed = table_name in metadata
            metadata = create_table(metadata, table_name, columns)
            if not existed and table_name in metadata:
                save_metadata("db_meta.json", metadata)
        elif command == "drop_table":
            if len(args) != 2:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[1]
            existed = table_name in metadata
            metadata = drop_table(metadata, table_name)
            if existed and table_name not in metadata:
                save_metadata("db_meta.json", metadata)
        elif command == "info":
            if len(args) != 2:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            table_data = load_table_data(table_name)
            columns_text = ", ".join(metadata[table_name])
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {columns_text}")
            print(f"Количество записей: {len(table_data)}")
        elif command == "insert":
            if len(args) < 4 or args[1] != "into" or "values" not in args:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[2]
            values = parse_values(user_input)
            if values is None:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_data = load_table_data(table_name)
            old_count = len(table_data)
            table_data = insert(metadata, table_name, values, table_data)
            if len(table_data) > old_count:
                save_table_data(table_name, table_data)
        elif command == "select":
            if len(args) < 3 or args[1] != "from":
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[2]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            where_clause = None
            if "where" in args:
                where_text = user_input.split("where", 1)[1].strip()
                if "=" not in where_text:
                    print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                    continue
                where_clause = parse_where(where_text)
            table_data = load_table_data(table_name)
            rows = select(table_data, where_clause)
            show_table(metadata, table_name, rows)
        elif command == "update":
            if len(args) < 6 or "set" not in args or "where" not in args:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            set_text = user_input.split("set", 1)[1].split("where", 1)[0].strip()
            where_text = user_input.split("where", 1)[1].strip()
            if "=" not in set_text or "=" not in where_text:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            set_clause = parse_set(set_text)
            where_clause = parse_where(where_text)
            table_data = load_table_data(table_name)
            table_data = update(table_data, set_clause, where_clause, table_name)
            save_table_data(table_name, table_data)
        elif command == "delete":
            if len(args) < 4 or args[1] != "from" or "where" not in args:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[2]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            where_text = user_input.split("where", 1)[1].strip()
            if "=" not in where_text:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            where_clause = parse_where(where_text)
            table_data = load_table_data(table_name)
            table_data = delete(table_data, where_clause, table_name)
            save_table_data(table_name, table_data)
        else:
            print(f"Функции {command} нет. Попробуйте снова.")