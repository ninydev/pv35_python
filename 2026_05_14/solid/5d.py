# 5. D — Dependency Inversion Principle


# class StripeAPI:
#     def pay(self, amount):
#         print(f"Оплата {amount} через Stripe")
#
# class Store:
#     def __init__(self):
#         self.payment_processor = StripeAPI() # Жесткая зависимость!
#
#     def checkout(self, amount):
#         self.payment_processor.pay(amount)



from abc import ABC, abstractmethod

# Абстракция (розетка)
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# Детали реализации
class StripeAPI(PaymentProcessor):
    def pay(self, amount):
        print(f"Оплата {amount} через Stripe")

class PayPalAPI(PaymentProcessor):
    def pay(self, amount):
        print(f"Оплата {amount} через PayPal")

# Класс верхнего уровня
class Store:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor # Зависим от абстракции!

    def checkout(self, amount):
        self.processor.pay(amount)

# Использование (инъекция зависимостей)
store = Store(PayPalAPI())
store.checkout(100)