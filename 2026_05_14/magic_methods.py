class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    # Магический метод для красивого вывода в print()
    def __str__(self):
        return f"Книга «{self.title}» ({self.pages} стр.)"

    # Магический метод для оператора " + " (__add__)
    def __add__(self, other):
        # Возвращаем общее количество страниц двух книг
        return self.pages + other.pages

    # Магический метод для оператора " > " (__gt__ / greater than)
    def __gt__(self, other):
        return self.pages > other.pages

book1 = Book("Гарри Поттер", 500)
book2 = Book("Властелин Колец", 700)

# 1. Благодаря __str__ мы видим не кракозябры памяти, а красивый текст!
print(book1)

# 2. Благодаря __add__ Питон научился складывать объекты!
total_pages = book1 + book2
print(f"Всего читать: {total_pages} страниц")

# 3. Благодаря __gt__ Питон умеет их сравнивать!
if book2 > book1:
    print(f"Книга «{book2.title}» толще!")