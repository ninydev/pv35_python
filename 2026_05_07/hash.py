import hashlib
import zlib

print(hashlib.md5(b"Hello World").hexdigest())
print(hashlib.sha1(b"Hello World").hexdigest())
print(hashlib.sha256(b"Hello World").hexdigest())
print(hashlib.sha3_256(b"Hello World").hexdigest())
print(hashlib.sha384(b"Hello World").hexdigest())
print(hashlib.blake2b(b"Hello World").hexdigest())

print("------------------")
print(zlib.crc32(b"Hello World"))


# print(hash("Hello World"))
# print(hash("Hello World"))
# print(hash("World Hello"))


# def simpleHash (text):
#     hash = 0
#     for char in text:
#         hash += ord(char)
#     return hash
#
# def otherHash (text):
#     hash = 0
#     c = 1
#     for char in text:
#         hash += ord(char) * c
#         c = c+ 1
#     return hash
#
#
# print(simpleHash("Hello World"))
# print(simpleHash("Hello World"))
# print(simpleHash("World Hello"))
#
# print(otherHash("Hello World"))
# print(otherHash("Hello World"))
# print(otherHash("World Hello"))