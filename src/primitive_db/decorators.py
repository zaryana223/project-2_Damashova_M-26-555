import time

from primitive_db.constants import CONFIRM_YES


def handle_db_errors(func):
    """Ловит ошибку функции и печатает сообщение."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper


def confirm_action(action_name):
    """Спрашивает подтверждение перед опасным действием."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]:'
            answer = input(text)
            if answer == CONFIRM_YES:
                return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func):
    """Печатает, сколько секунд выполнялась функция."""
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        finish = time.monotonic()
        seconds = finish - start
        print(f"Функция {func.__name__} выполнилась за {seconds:.3f} секунд.")
        return result
    return wrapper


def create_cacher():
    """Возвращает функцию, которая помнит результаты запросов."""
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result