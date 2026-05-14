# 2. O — Open/Closed Principle

# class DiscountCalculator:
#     def calculate(self, customer_type, price):
#         if customer_type == "regular":
#             return price * 0.9
#         elif customer_type == "premium":
#             return price * 0.8
#         return price


class Discount:
    def calculate(self, price):
        return price

class RegularDiscount(Discount):
    def calculate(self, price):
        return price * 0.9

class PremiumDiscount(Discount):
    def calculate(self, price):
        return price * 0.8

# Мы просто передаем нужный класс скидки
def get_final_price(price, discount_strategy: Discount):
    return discount_strategy.calculate(price)