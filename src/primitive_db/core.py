def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    allowed = ["int", "str", "bool"]
    new_columns = []
    has_id = False
    for column in columns:
        parts = column.split(":")
        if len(parts) != 2 or parts[1] not in allowed:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
        if parts[0] == "ID":
            has_id = True
        new_columns.append(column)

    if not has_id:
        new_columns.insert(0, "ID:int")

    metadata[table_name] = new_columns
    columns_text = ", ".join(new_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_text}')
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def insert(metadata, table_name, values, table_data):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    columns = []
    for column in metadata[table_name]:
        parts = column.split(":")
        if parts[0] != "ID":
            columns.append(parts)

    if len(values) != len(columns):
        print(f"Некорректное значение: {values}. Попробуйте снова.")
        return table_data

    new_id = 0
    for item in table_data:
        if item["ID"] > new_id:
            new_id = item["ID"]

    row = {"ID": new_id + 1}
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
    print(f'Запись с ID={row["ID"]} успешно добавлена в таблицу "{table_name}".')
    return table_data


def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    result = []
    for row in table_data:
        match = True
        for key in where_clause:
            if key not in row or row[key] != where_clause[key]:
                match = False
        if match:
            result.append(row)
    return result


def update(table_data, set_clause, where_clause, table_name):
    for row in table_data:
        match = True
        for key in where_clause:
            if key not in row or row[key] != where_clause[key]:
                match = False
        if match:
            for key in set_clause:
                row[key] = set_clause[key]
            print(
                f'Запись с ID={row["ID"]} в таблице "{table_name}" успешно обновлена.'
                )
    return table_data


def delete(table_data, where_clause, table_name):
    new_data = []
    for row in table_data:
        match = True
        for key in where_clause:
            if key not in row or row[key] != where_clause[key]:
                match = False
        if match:
            print(
                f'Запись с ID={row["ID"]} успешно удалена из таблицы "{table_name}".'
                )
        else:
            new_data.append(row)
    return new_data