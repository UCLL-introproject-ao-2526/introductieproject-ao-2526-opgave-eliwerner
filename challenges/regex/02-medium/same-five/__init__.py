import re

# Regex voor 'vijf dezelfde karakters achter elkaar'
pattern = r"(.)\1{4}"

# Teststrings
tests = [
    "aaaaa",       # ✅ match
    "baaaaa",      # ✅ match
    "aaaaab",      # ✅ match
    "cbaaaaae",    # ✅ match
    "aaaa",        # ❌ geen match
    "aaabaaa",     # ❌ geen match
    "11111",       # ✅ match
    "ab11111cd",   # ✅ match
]

# Functie om te checken
def check(string):
    return bool(re.search(pattern, string))

# Test uitvoeren
for s in tests:
    print(s, "->", check(s))
