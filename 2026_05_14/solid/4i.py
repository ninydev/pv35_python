# 4. I — Interface Segregation Principle

# class WorkerInterface:
#     def work(self): pass
#     def eat(self): pass
#
#
# class Robot(WorkerInterface):
#     def work(self):
#         print("Робот работает")
#
#     def eat(self):
#         # Нарушение: Роботу не нужна еда!
#         pass


class Workable:
    def work(self): pass

class Eatable:
    def eat(self): pass

class Human(Workable, Eatable):
    def work(self): print("Человек работает")
    def eat(self): print("Человек ест")

class Robot(Workable):
    def work(self): print("Робот работает")
    # Робот не наследует Eatable, все счастливы