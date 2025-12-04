import re

def check(hehe):
    return bool(re.match(r'^.{5}$', hehe))


# Testen
print(check("abcde"))  # True, precies 5 tekens
print(check("abcd"))   # False, te kort
print(check("abcdef")) # False, te lang