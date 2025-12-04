import re

# Regex: exact drie plusjes in de string, mag andere tekens hebben, geen meer of minder
pattern = r'^(?:[^+]*\+){3}[^+]*$'

def check(s):
    return bool(re.fullmatch(pattern, s))

# Lijst van strings die geaccepteerd moeten worden
accepted = [
    "+++",
    "1+2+3+4",
    "+1+2+",
    "aaaa+bbbbb+ccccc+ddddd",
    "a+++",
    "+++b",
    "+5+a+"
]

# Lijst van strings die afgewezen moeten worden
rejected = [
    "",
    "+",
    "++",
    "++++",
    "+++++"
]

for s in accepted:
    print(s, "->", check(s))

print("----------")


for s in rejected:
    print(s, "->", check(s))

