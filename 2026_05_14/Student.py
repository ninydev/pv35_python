

class Student:

    # def __init__(self):
    #     self.name = ""
    #     self.age = 0



    def __init__(self, name, age):
        self.name = name
        self.age = age
        self._iprotected = 'protected'
        self.__iprivate = 'private'


    def introduce(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")


    def __str__(self):
        return f"Student(name={self.name}, age={self.age})"

