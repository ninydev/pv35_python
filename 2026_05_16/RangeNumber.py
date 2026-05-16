class RangeNumber:
    def __init__(self, name, min, max):
        self.name = name
        self.__min = min
        self.__max = max


    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value < self.__min:
            raise ValueError(f"{self.name} cannot be less than {self.__min}")
        if value > self.__max:
            raise ValueError(f"{self.name} cannot be more than {self.__max}")
        instance.__dict__[self.name] = value

