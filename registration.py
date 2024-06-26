import csv
import utils

from db import *


def parse_team_row(row, db):
    members = utils.get_members(row, n=utils.N_IN_TEAM)
    teamid = row[utils.TEAM_ID_IND]
    ids, surnames_ar = [], []
    for member in members:
        if member["surname"] is None:
            continue
        stmt = make_stmt(member)
        if db.execute(stmt).first() is None:
            db_member = make_db_member(member)
            db_member.send_mail = True
            db.add(db_member)
            db.commit()
        res = db.execute(stmt).first()[0]
        surnames_ar.append(res.surname)
        ids.append(res.id)
    ids += [0] * (3 - len(ids))
    surnames = ", ".join(sorted(surnames_ar))
    stmt = select(Team).where(Team.surnames == surnames)
    if db.execute(stmt).first() is None:
        db_team = Team(
            id1=ids[0],
            id2=ids[1],
            id3=ids[2],
            surnames=surnames,
            teamname=make_teamname(teamid, surnames),
            login=utils.gen_handle(teamid, base="maiop"),
            password=utils.gen_password(utils.PASS_LEN),
        )
        db.add(db_team)
        db.commit()


def parse_junior_row(row, db, login_base):
    member = utils.get_members(row, n=1)[0]
    last_db_member = db.query(Member).order_by(Member.id.desc()).first()
    last_id = 1 if last_db_member is None else last_db_member.id + 1
    member["login"] = utils.gen_handle(last_id, base=login_base)
    member["password"] = utils.gen_password(utils.PASS_LEN)
    stmt = make_stmt(member)
    if db.execute(stmt).first() is None:
        db.add(make_db_member(member))
        db.commit()


def parse_table_row(row, db, mode="teams"):
    if mode == "teams":
        parse_team_row(row, db)
    elif mode == "juniors" or mode == "summer":
        parse_junior_row(row, db, mode)


def register_pg(fname_in="registration.csv", mode="teams"):
    pg = make_session()
    with open(fname_in, "r") as fin_csv:
        fin = csv.reader(fin_csv)
        next(fin)
        for row in fin:
            parse_table_row(row, pg, mode=mode)
