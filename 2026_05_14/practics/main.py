from ConsoleUI import ConsoleUI
from HumanRepository import HumanRepository


repo = HumanRepository()
app = ConsoleUI(repo)
app.run()