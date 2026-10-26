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