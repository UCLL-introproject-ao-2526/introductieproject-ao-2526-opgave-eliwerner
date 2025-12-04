import re


def check(hehe):
    return bool(re.fullmatch(r'\d\d:\d\d', hehe))


print(check("21:34"))
print(check("7:34"))

