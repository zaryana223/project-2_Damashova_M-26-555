# project-2_Damashova_M-26-555
Работу выполнила Дамашова Заряна Алексеевна
## Управление таблицами

**`database`**

Запускает базу данных в терминале и показывает справочную информацию о командах.

**`create_table <имя_таблицы> <столбец:тип> ...`**

Создает таблицу. После имени таблицы идут столбцы в виде `имя:тип`. Типов только три: `int`, `str`, `bool`. Если столбец `ID` не указан, программа сама ставит `ID:int` первым.

**`list_tables`**

Показывает все таблицы, которые уже созданы. Каждая печатается с новой строки: `- users`.

**`drop_table <имя_таблицы>`**

Удаляет таблицу с этим именем. Если таблицы нет, программа пишет, что она не существует.

**`help`**

Повторно выводит справку со списком команд.

**`exit`**

Закрывает программу и возвращает обычную строку терминала.

Пример:

    (primitive-db) PS C:\Users\Z10damashova\Documents\project-2_Damashova_M-26-555> database

    ***Процесс работы с таблицей***
    Функции:
    <command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу
    <command> list_tables - показать список всех таблиц
    <command> drop_table <имя_таблицы> - удалить таблицу

    Общие команды:
    <command> exit - выход из программы
    <command> help - справочная информация

    Введите команду: create_table users name:str age:int is_active:bool
    Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool
    Введите команду: create_table users name:str
    Ошибка: Таблица "users" уже существует.
    Введите команду: list_tables
    - users
    Введите команду: drop_table users
    Таблица "users" успешно удалена.
    Введите команду: drop_table products
    Ошибка: Таблица "products" не существует.
    Введите команду: exit
    (primitive-db) PS C:\Users\Z10damashova\Documents\project-2_Damashova_M-26-555>

## Запись работы

[![asciicast](https://asciinema.org/a/iGa0btukdKXGvqWE.svg)](https://asciinema.org/a/iGa0btukdKXGvqWE)