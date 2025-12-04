import re

def check(hehe):
    return bool(re.findall(r'[a-zA-Z]+', hehe))


print(check("hello WORLD"))

