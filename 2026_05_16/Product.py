from PositiveNumber import PositiveNumber

class Product:

    price = PositiveNumber('price')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"Product(name={self.name}, price={self.price})"