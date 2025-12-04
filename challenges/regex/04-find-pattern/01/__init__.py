import re

pattern = r'^0(10)*1?$'

def check(s):
    return bool(re.fullmatch(pattern, s))

tests = [
    "0",
    "01",
    "010",
    "0101",
    "01010",
    "",        # should be False
    "1",       # False
    "00",      # False
    "11",      # False
    "10102",   # False
    "1001010101"  # False
]

for t in tests:
    print(t, "->", check(t))
    
