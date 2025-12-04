import re

def check(hehe):
    return bool(re.fullmatch(r'(a+b)*(c+d)+1', hehe))


print(check("cd1"))

print(check("ab1"))

