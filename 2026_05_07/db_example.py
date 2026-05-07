import hashlib

users ={
    'keeper@ninydev.com' : {
        'password' : hashlib.md5('Qwerty123'.encode()).hexdigest(),
        'name' : 'Keeper',
        'age' : 50},
    'sveta@ninydev.com': {
        'password' : hashlib.md5('Qwerty123'.encode()).hexdigest(),
        'name' : 'Sveta',
        'age' : 25}
}
print(users)
print("---------------------------")

bigUserIterator = filter (lambda x: x['age'] >= 30, users.values())
for user in bigUserIterator:
    print(f"User: {user['name']}, Age: {user['age']}")

print("---------------------------")
print(users.items())

otherIterator = filter (lambda x: x[1]['age'] >= 30, users.items())

print("---------------------------")
print (dict(otherIterator))
# for user in bigUserIterator:
#     print (user)
#     print (type(user))
# #    print(f"User: {user[1]['name']}, Age: {user[1]['age']}")

# print (users)
#
# for user in users.values():
#     print(f"User: {user['name']}, Age: {user['age']}")
#     if user['age'] > 30:
#         print(f"{user['name']} is an adult")
#



#---------------------------------------------------------------------
# usersBook = [
#     {'name': 'Hanna', 'age': 10, 'login':'user56'},
#     {'name': 'Mark', 'age': 15, 'login':'usER111'},
#     {'name': 'Jane', 'age': 19, 'login':'superGirl'},
#     {'name': 'Jack', 'age': 27, 'login':'userJack'}
# ]
#
# print(usersBook)
#
# adultUsers = list(filter(lambda x: x['age'] >= 18, usersBook))
# print(adultUsers)
#
# iterator = filter(lambda x: x['age'] >= 18, usersBook)
# for user in iterator:
#     print(user)


# # sortedByName = sorted(usersBook, key=lambda x: x['name'])
# # print(sortedByName)
# #
# # sortedByAge = sorted(usersBook, key=lambda x: x['age'])
# # print(sortedByAge)
#
# # usersBook.sort(key=lambda x: x['age'])
#
# print(usersBook)
