import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata


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
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


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
        else:
            print(f"Функции {command} нет. Попробуйте снова.")