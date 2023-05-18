import re

groups = {
    "1b": "1([0-9]{2})Б",
    "2b": "2([0-9]{2})Б",
    "3b": "3([0-9]{2})Б",
    "4b": "4([0-9]{2})Б",
    "1m": "1([0-9]{2})М",
    "2m": "2([0-9]{2})М",
}


def check(s, pattern):
    return False if re.search(groups[pattern], s) is None else True
