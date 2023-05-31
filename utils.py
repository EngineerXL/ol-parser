import requests


def save_from_url(url=None, fname=None):
    if url and fname:
        r = requests.get(url)
        r.encoding = "utf-8"
        with open(fname, "w") as fout:
            fout.write(r.text)


def count_solved(ar):
    res = 0
    for elem in ar:
        if "+" in elem:
            res += 1
    return res


def get_value(s):
    t = s.strip()
    return None if t == "-" else t


# В названии команды могут быть скобки, а фамилии всегда с конца
def get_surnames_ar(s):
    t = s.strip()[::-1]
    beg, end = t.find(")"), t.find("(")
    if beg == -1:
        raise BaseException(('Could not resolve team name: "%s"' % s))
    ar = t[beg + 1 : end][::-1].replace(",", "")
    return sorted(ar.split())


OFFSET = 1
MEMBER_SZ = 7


def get_members(row, n=3):
    res = [dict() for _ in range(n)]
    for i in range(n):
        res[i]["surname"] = get_value(row[OFFSET + MEMBER_SZ * i + 0])
        res[i]["firstname"] = get_value(row[OFFSET + MEMBER_SZ * i + 1])
        res[i]["middlename"] = get_value(row[OFFSET + MEMBER_SZ * i + 2])
        res[i]["group"] = get_value(row[OFFSET + MEMBER_SZ * i + 3])
    return res
