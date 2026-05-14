class RepositoryInterface:
    def create(self, data):
        raise NotImplementedError("Метод create() не реалізований")

    def readAll(self):
        raise NotImplementedError("Метод readAll() не реалізований")

    def read(self, id):
        raise NotImplementedError("Метод read() не реалізований")

    def update(self, id, data):
        raise NotImplementedError("Метод update() не реалізований")

    def delete(self, id):
        raise NotImplementedError("Метод delete() не реалізований")
