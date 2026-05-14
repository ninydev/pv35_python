from HumanEntity import HumanEntity
from CommandInterface import CommandInterface

class ShowHumansCommand(CommandInterface):
    def __init__(self, repository):
        self.repo = repository

    def execute(self):
        print("\n--- Список всех людей ---")
        humans = self.repo.readAll()
        if not humans:
            print("База данных пуста.")
            return

        for index, human in enumerate(humans):
            print(f"[{index}] {human}")