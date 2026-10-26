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

[![asciicast](https://asciinema.org/a/iGa0btukdKXGvqWE.png)](https://asciinema.org/a/iGa0btukdKXGvqWE)

## CRUD-операции

**`insert into <имя_таблицы> values (<значение1>, <значение2>, ...)`**

Добавляет запись. Значение `ID` вводить не нужно, программа ставит его сама. Остальные поля обязательны. Текст пишется в кавычках, число как число, логическое значение как `true` или `false`.

**`select from <имя_таблицы>`**

Показывает все записи таблицы.

**`select from <имя_таблицы> where <столбец> = <значение>`**

Показывает только те записи, где столбец равен значению.

**`update <имя_таблицы> set <столбец> = <новое_значение> where <столбец_условия> = <значение_условия>`**

Меняет поле в записях таблицы, которые подходят под условие.

**`delete from <имя_таблицы> where <столбец> = <значение>`**

Удаляет записи из таблицы, которые подходят под условие.

**`info <имя_таблицы>`**

Показывает три строки: имя таблицы, столбцы в виде `имя:тип` и число записей. Если записей нет, последняя строка будет `Количество записей: 0`.

Пример:

    PS C:\Users\Z10damashova\Documents\project-2_Damashova_M-26-555> uv run database

    ***Операции с данными***
    Функции:
    <command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.
    <command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.
    <command> select from <имя_таблицы> - прочитать все записи.
    <command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.
    <command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.
    <command> info <имя_таблицы> - вывести информацию о таблице.
    <command> exit - выход из программы
    <command> help- справочная информация

    Введите команду: create_table users name:str age:int is_active:bool
    Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool
    Введите команду: insert into users values ("Sergei", 28, true)
    Запись с ID=1 успешно добавлена в таблицу "users".
    Введите команду: select from users where age = 28
    +----+--------+-----+-----------+
    | ID |  name  | age | is_active |
    +----+--------+-----+-----------+
    | 1  | Sergei |  28 |    True   |
    +----+--------+-----+-----------+
    Введите команду: update users set age = 29 where name = "Sergei"
    Запись с ID=1 в таблице "users" успешно обновлена.
    Введите команду: delete from users where ID = 1
    Запись с ID=1 успешно удалена из таблицы "users".
    Введите команду: info users
    Таблица: users
    Столбцы: ID:int, name:str, age:int, is_active:bool
    Количество записей: 0
    Введите команду: exit
    PS C:\Users\Z10damashova\Documents\project-2_Damashova_M-26-555>

## Запись CRUD-операций

[![asciicast](https://asciinema.org/a/ASvGwEFVGeiWuxPx.png)](https://asciinema.org/a/ASvGwEFVGeiWuxPx)