class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_info(self):
        return f"Меня зовут {self.name}, мне {self.age} лет."