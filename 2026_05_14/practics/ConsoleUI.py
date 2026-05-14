from HumanRepository import HumanRepository
from AddHumanCommand import AddHumanCommand
from ShowHumansCommand import ShowHumansCommand
from ExitCommand import ExitCommand


class ConsoleUI:
    def __init__(self, repository):
        # Инициализируем словарь, где ключи - это ввод пользователя,
        # а значения - ЭКЗЕМПЛЯРЫ классов-команд.
        self.commands = {
            '1': AddHumanCommand(repository),
            '2': ShowHumansCommand(repository),
            '0': ExitCommand()
        }

    def run(self):
        print("=== Добро пожаловать в Базу Данных ===")
        while True:
            print("\nДоступные команды: 1:Добавить | 2:Показать | 3:Удалить | 0:Выход")
            user_input = input("Выберите действие: ").strip()

            # Достаем нужную команду из словаря
            command = self.commands.get(user_input)

            if command:
                # Запускаем метод execute() найденной команды
                command.execute()
            else:
                print("❌ Неизвестная команда. Попробуйте снова.")