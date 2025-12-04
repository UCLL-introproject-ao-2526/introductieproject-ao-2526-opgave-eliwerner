import re

def check_dot(s):
    return bool(re.fullmatch(r'\.', s))



print(check_dot("."))
print(check_dot("a"))
print(check_dot(".."))

