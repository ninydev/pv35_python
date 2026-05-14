from CommandInterface import CommandInterface


class ExitCommand(CommandInterface):
    def execute(self):
        print("Завершение работы...")
        exit(0)