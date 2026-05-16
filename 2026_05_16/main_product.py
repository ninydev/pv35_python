from Product import Product

samsung = Product('S25', 29500)


print(samsung)

try:
    samsung.price = -10
except Exception as e:
    print(e)

print('--------------------')

print(samsung)