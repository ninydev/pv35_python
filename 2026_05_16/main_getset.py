from UserGetSet import UserGetSet

keeper = UserGetSet("Keeper", 49)

print('--------------------')
keeper.name = "Oleksandr Nykytin"
print(keeper.name)

keeper._name = "Vasya"
print(keeper.name)

try:
    keeper.age=-10
except Exception as e:
    print(e)

print('--------------------')
print(keeper.age)


keeper._age = -10
print(keeper.age)

print(keeper._p)