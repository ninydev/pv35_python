# 1. Определяем множества
white_wool = {"Шон", "Облачко", "Зевс", "Снежок"}
blue_eyes = {"Шон", "Облачко", "Титан", "Пират"}
has_horns = {"Шон", "Зевс", "Титан", "Блэкки"}

# 2. Практика:
# Кто самый крутой (белый, голубоглазый и с рогами)?
the_best = white_wool & blue_eyes & has_horns
print(f"Самый крутой: {the_best}")  # {'Шон'}

# Кто белый и голубоглазый, но БЕЗ рожек?
cute_ones = (white_wool & blue_eyes) - has_horns
print(f"Милашки: {cute_ones}")      # {'Облачко'}

# Список всех барашков, у которых есть ХОТЯ БЫ ОДИН признак из наших кругов - U
any_feature = white_wool | blue_eyes | has_horns
print(f"Всего в кругах: {len(any_feature)} барашков")
