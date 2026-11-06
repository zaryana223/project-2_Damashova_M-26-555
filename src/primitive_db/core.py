from primitive_db.constants import ID_COLUMN, ID_FIELD, VALID_TYPES
from primitive_db.decorators import (
    confirm_action,
    create_cacher,
    handle_db_errors,
    log_time,
)

cache_result = create_cacher()

@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает таблицу и сама добавляет столбец ID, если его нет."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    allowed = VALID_TYPES
    new_columns = []
    has_id = False
    for column in columns:
        parts = column.split(":")
        if len(parts) != 2 or parts[1] not in allowed:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
        if parts[0] == ID_FIELD:
            has_id = True
        new_columns.append(column)

    if not has_id:
        new_columns.insert(0, ID_COLUMN)

    metadata[table_name] = new_columns
    columns_text = ", ".join(new_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_text}')
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values, table_data):
    """Добавляет запись и ставит новый ID."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = []
    for column in metadata[table_name]:
        parts = column.split(":")
        if parts[0] != ID_FIELD:
            columns.append(parts)

    if len(values) != len(columns):
        print(f"Некорректное значение: {values}. Попробуйте снова.")
        return table_data

    new_id = 0
    for item in table_data:
        if item[ID_FIELD] > new_id:
            new_id = item[ID_FIELD]

    row = {ID_FIELD: new_id + 1}
    for i in range(len(columns)):
        name = columns[i][0]
        type_name = columns[i][1]
        value = values[i]
        if type_name == "int" and type(value) is int:
            row[name] = value
        elif type_name == "str" and type(value) is str:
            row[name] = value
        elif type_name == "bool" and type(value) is bool:
            row[name] = value
        else:
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return table_data

    table_data.append(row)
    print(f'Запись с ID={row[ID_FIELD]} успешно добавлена в таблицу "{table_name}".')
    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает записи. Повтор того же запроса берет из памяти."""
    def get_rows():
        if where_clause is None:
            return table_data

        result = []
        for row in table_data:
            match = True
            for column in where_clause:
                if column not in row or row[column] != where_clause[column]:
                    match = False
            if match:
                result.append(row)
        return result

    query_key = str(table_data) + str(where_clause)
    return cache_result(query_key, get_rows)


@handle_db_errors
def update(table_data, set_clause, where_clause, table_name):
    """Меняет поля в записях, которые подходят под условие."""
    for row in table_data:
        match = True
        for key in where_clause:
            if key not in row or row[key] != where_clause[key]:
                match = False
        if match:
            for key in set_clause:
                row[key] = set_clause[key]
            print(
                f'Запись с ID={row[ID_FIELD]} '
                f'в таблице "{table_name}" успешно обновлена.'
                )
    return table_data


@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause, table_name):
    """Удаляет записи, которые подходят под условие."""
    new_data = []
    for row in table_data:
        match = True
        for key in where_clause:
            if key not in row or row[key] != where_clause[key]:
                match = False
        if match:
            print(
                f'Запись с ID={row[ID_FIELD]} '
                f'успешно удалена из таблицы "{table_name}".'
                )
        else:
            new_data.append(row)
    return new_data