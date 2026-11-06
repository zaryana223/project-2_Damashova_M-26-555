import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загружает метаданные из JSON. Если файла нет, возвращает пустой словарь."""
    try:
        with open(filepath, encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)


def load_table_data(table_name):
    """Загружает записи таблицы. Если файла нет, возвращает пустой список."""
    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath, encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет записи таблицы в JSON-файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)


def delete_table_data(table_name):
    """Удаляет JSON-файл таблицы, если он есть."""
    filepath = f"{DATA_DIR}/{table_name}.json"
    if os.path.exists(filepath):
        os.remove(filepath)