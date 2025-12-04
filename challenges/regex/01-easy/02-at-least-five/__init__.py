import re


def matches(string):
    return  bool(re.fullmatch(r'.{5,}', string))



print(matches("12345"))
print(matches("123"))


