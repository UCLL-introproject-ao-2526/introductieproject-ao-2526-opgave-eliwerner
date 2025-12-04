import re

pattern = r'^(.)(?!\1).$'

def check(s):
    return bool(re.fullmatch(pattern, s))

tests = [
    "ab",   # True
    "A2",   # True
    "41",   # True
    "9X",   # True
    "71",   # True
    "",     # False
    "x",    # False
    "312",  # False
    "aa",   # False
    "99",   # False
]

for t in tests:
    print(t, "->", check(t))


