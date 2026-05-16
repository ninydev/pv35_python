class ErrorNum:
    def __init__(self, name):
        self.name = name
        self.__value = 0

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} cannot be negative")
        self.__value = value

e = ErrorNum('value')
e.value = 10
print(e.value)

try:
    e.value = -10
except Exception as e:
    print(e)

print(e.value)