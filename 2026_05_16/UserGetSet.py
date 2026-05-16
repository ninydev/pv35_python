class UserGetSet:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self._p = 'protected'

    @property
    def name(self):
        print("Getting name")
        return self._name

    @name.setter
    def name(self, value):
        print("Setting name")
        self._name = value

    @property
    def age(self):
        print("Getting age")
        return self._age

    @age.setter
    def age(self, value):
        print("Setting age")
        if (value < 0):
            raise ValueError("Age cannot be negative")
        self._age = value