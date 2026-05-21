from ProductClass import ProductClass
from ProductDataClass import ProductDataClass

pc1 = ProductClass('s25', 29700)
pc2 = ProductClass('s25', 29700)

pds1 = ProductDataClass('s25', 29700)
pds2 = ProductDataClass('s25', 29700)

print(f'ProductClass: {pc1 == pc2}')
print(f'ProductDataClass: {pds1 == pds2}')