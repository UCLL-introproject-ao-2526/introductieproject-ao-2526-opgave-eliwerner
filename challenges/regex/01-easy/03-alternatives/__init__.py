import re

def check(hehe):
    return bool(re.fullmatch(r'[aeiouAEIOU]', hehe))


print(check("a"))
print(check("E"))

print(check("Ae"))



