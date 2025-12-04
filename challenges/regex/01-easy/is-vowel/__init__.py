import re

def check(hehe):
    return bool(re.fullmatch(r'[AEIOUaeiou]', hehe))


print(check("A"))  # True
print(check("e"))  # True
print(check("b"))  # False
print(check("AE")) # False