from itertools import count

sites = ("Gerc", "Komunalka")
mobileApp = ("GercMob", "KomunaMob")

allProjects = sites + mobileApp

print(allProjects)
print(type(allProjects))

print(allProjects.count("Komunalka"))
print(allProjects.index("Komunalka"))

if allProjects.index("Komunalka") > 0:
    print("Komunalka is present in the tuple")

if 'Komunalka' in allProjects:
    print("Komunalka is present in the tuple")

*lstProjects, = allProjects
print(lstProjects)
print(type(lstProjects))
if 'Komunalka' in lstProjects:
    print("Komunalka is present in the list")


# userTypes = ('admin', 'student', 'teacher', 'moderator')
#
# for userType in userTypes:
#     print(userType)
#     print(type(userType))


# print(userTypes)
# print(type(userTypes))
#
#
# admin, *users, moderator = userTypes
# print(admin) #admin
# print(type(admin))
#
# print(users) #['student', 'teacher', 'moderator']
# print(type(users))


# Example
# user1, user2, user3, user4 = userTypes
#
#
# print(user1) #admin
# print(user2) #student
# print(user3) #teacher
# print(user4) #moderator
#
# user1 = "superAdmin"
#
# newUserTypes = (user1, user2, user3, user4)
# print(newUserTypes) #('superAdmin', 'student', 'teacher', 'moderator')




# # status enum('new', 'success', 'error', 'reverse', 'timeout', 'in_processing')
#
#
# documentStatus = "In Progress", "Needs Review", "Completed"
#
# print(documentStatus[0])
# # documentStatus[5] = "Draft"
# # print(documentStatus)
#
#
#
#
# # ConnectionString=("MySql://localhost:3306/test",)
# # print(ConnectionString)
# # print(type(ConnectionString))
