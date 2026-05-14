# Реалізуйте клас «Людина».
# Збережіть у класі: ПІБ, дату народження, контактний телефон, місто, країну, домашню адресу.
# Реалізуйте методи класу для введення-виведення даних та інших операцій.


class HumanEntity:
    def __init__(self, name, birthdate, phone, email, city, country, address):
        self.name = name
        self.birthdate = birthdate
        self.phone = phone
        self.email=email
        self.city = city
        self.country = country
        self.address = address

    def __str__(self):
        return f"Ім'я: {self.name}, Дата народження: {self.birthdate}, Телефон: {self.phone}, Місто: {self.city}, Країна: {self.country}, Адреса: {self.address}"
