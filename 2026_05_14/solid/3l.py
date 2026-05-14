# 3. L — Liskov Substitution Principle (

# class Bird:
#     def fly(self):
#         print("Я лечу!")
#
# class Penguin(Bird):
#     def fly(self):
#         raise Exception("Пингвины не летают!")
#
# def let_bird_fly(bird: Bird):
#     bird.fly() # Программа упадет, если передать Penguin


class Bird:
    pass

class FlyingBird(Bird):
    def fly(self):
        print("Я лечу!")

class NonFlyingBird(Bird):
    def walk(self):
        print("Я иду пешком.")

class Penguin(NonFlyingBird):
    pass