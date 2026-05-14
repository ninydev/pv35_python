from HumanEntity import HumanEntity
from CommandInterface import CommandInterface


class AddHumanCommand(CommandInterface):
    def __init__(self, repository):
        self.repo = repository

    def execute(self):
        print("\n--- Добавление нового человека ---")
        name = input("Введите ПІБ: ")
        birthdate = input("Введите дату рождения: ")
        phone = input("Введите телефон: ")
        email = input("Введите email: ")
        city = input("Введите город: ")
        country = input("Введите страну: ")
        address = input("Введите адрес: ")

        new_human = HumanEntity(name, birthdate, phone, email, city, country, address)
        self.repo.create(new_human)
        print("✅ Человек успешно добавлен!")