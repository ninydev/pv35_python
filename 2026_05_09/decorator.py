import time

# Эмулируем наш Redis (быстрая память) обычным словарем
redis_cache = {}


# 1. ПИШЕМ ДЕКОРАТОР-КЭШ
def with_redis_cache(func):
    def wrapper(city_id):
        # ШАГ 1: Спрашиваем у Redis
        if city_id in redis_cache:
            print(f"⚡ [REDIS] Город {city_id} найден в кэше! Моментальная отдача.")
            return redis_cache[city_id]

        # ШАГ 2: Если в Redis пусто — дергаем оригинальную SQL-функцию
        print(f"🐢 [SQL] В кэше пусто. Идем в тяжелую реляционную базу за {city_id}...")
        city_data = func(city_id)

        # ШАГ 3: Записываем полученный результат в Redis на будущее
        if city_data:
            redis_cache[city_id] = city_data
            print(f"💾 [REDIS] Город '{city_data}' успешно сохранен в кэш.")

        return city_data

    return wrapper


# 2. НАША БАЗОВАЯ ФУНКЦИЯ
# Она ничего не знает про Redis, просто честно ходит в SQL
@with_redis_cache
def get_city_from_sql(city_id):
    # Симулируем долгий ответ от базы данных (2 секунды)
    time.sleep(2)

    # Эмулируем SQL-базу
    sql_db = {
        1: "Киев",
        2: "Николаев",
        3: "Одесса"
    }

    return sql_db.get(city_id, "Город не найден")


# === ПРОВЕРЯЕМ В РАБОТЕ ===

print("--- ЗАПРОС 1 (Пользователь открыл страницу) ---")
# Отработает медленно, так как кэш пустой
print("Результат:", get_city_from_sql(2))

print("\n--- ЗАПРОС 2 (Тот же пользователь обновил страницу) ---")
# Отработает мгновенно, так как перехватит декоратор
print("Результат:", get_city_from_sql(2))

print("\n--- ЗАПРОС 3 (Запрос другого города) ---")
# Снова пойдет в SQL
print("Результат:", get_city_from_sql(1))