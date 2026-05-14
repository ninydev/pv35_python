from Person import Person

class Student(Person):

    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    # Добавляем свою уникальную фичу, которой нет у обычного Person
    def study(self):
        print(f"{self.name} усердно учит Python!")