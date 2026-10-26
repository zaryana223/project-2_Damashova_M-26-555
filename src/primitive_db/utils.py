import json
import os


def load_metadata(filepath):
    try:
        with open(filepath, encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)


def load_table_data(table_name):
    filepath = f"data/{table_name}.json"
    try:
        with open(filepath, encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    os.makedirs("data", exist_ok=True)
    filepath = f"data/{table_name}.json"
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file)