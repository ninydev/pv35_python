class BackpackCaller:
    def __init__(self, matches, salt):
        self.matches = matches
        self.salt = salt

    def __call__(self, action, amount=1):
        if action == "разжечь костер":
            if self.matches >= amount:
                self.matches -= amount
                print(f"🔥 Костер горит! Потрачено спичек: {amount}. Осталось: {self.matches}.")
            else:
                print("❌ Упс, спички закончились!")
        elif action == "посолить суп":
            if self.salt >= amount:
                self.salt -= amount
                print(f"🍲 Суп посолен! Потрачено соли: {amount}г. Осталось: {self.salt}")
            else:
                print("❌ Соли больше нет, суп будет пресным!")