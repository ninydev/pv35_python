from RepositoryInterface import RepositoryInterface

class HumanRepository (RepositoryInterface):
    def __init__(self):
        self.humans = []

    def create(self, data):
        self.humans.append(data)

    def readAll(self):
        return self.humans

    def read(self, id):
        return self.humans[id]

    def update(self, id, data):
        self.humans[id] = data

    def delete(self, id):
        del self.humans[id]


