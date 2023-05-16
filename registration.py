import csv
import utils

from db import *
from sqlalchemy import select


def register_to_csv(url=None, mode="teams", fname_out="registration.csv"):
    utils.save_from_url(url, fname_out)


def get_members(a):
    res = [["" for _ in range(4)] for _ in range(3)]
    for i in range(4):
        res[0][i] = a[1 + 0 + i].strip()
        res[1][i] = a[1 + 7 + i].strip()
        res[2][i] = a[1 + 14 + i].strip()
    return res


def parse_table_raw(row, db):
    members = get_members(row)
    ids, surnames_ar = [], []
    for elem in members:
        if elem[0] == "-":
            continue
        stmt = select(Member).where(
            Member.surname == elem[0],
            Member.firstname == elem[1],
            Member.middlename == elem[2],
            Member.group == elem[3],
        )
        if db.execute(stmt).first() is None:
            db_member = Member(
                surname=elem[0], firstname=elem[1], middlename=elem[2], group=elem[3]
            )
            db.add(db_member)
            db.commit()
        res = db.execute(stmt).first()[0]
        surnames_ar.append(res.surname)
        ids.append(res.id)
    ids += [0] * (3 - len(ids))
    surnames = ", ".join(sorted(surnames_ar))
    stmt = select(Team).where(Team.surnames == surnames)
    if db.execute(stmt).first() is None:
        db_team = Team(id1=ids[0], id2=ids[1], id3=ids[2], surnames=surnames)
        db.add(db_team)
        db.commit()


def register_pg(mode="teams", fname_in="registration.csv"):
    pg = make_session()
    with open(fname_in, "r") as fin_csv:
        fin = csv.reader(fin_csv)
        next(fin)
        for row in fin:
            parse_table_raw(row, pg)
