import csv
import groups_regex

from db import *
from sqlalchemy import select


def get_surnames_ar(s):
    pos = s.find("(")
    if pos == -1:
        raise BaseException(('Could not resolve team name: "%s"' % s))
    ar = s[pos + 1 : -1].replace(",", "")
    return sorted(ar.split())


def add_results(contestant_scores, id, key_base, doreshka, cnt):
    if id not in contestant_scores.keys():
        contestant_scores[id] = {
            "solved": 0,
            "upsolved": 0,
        }
        if key_base is not None:
            contestant_scores[id][key_base + "solved"] = 0
            contestant_scores[id][key_base + "upsolved"] = 0
    key = doreshka if key_base is None else key_base + doreshka
    contestant_scores[id][key] += cnt


def upd_team_results(s, db, contestant_scores, cnt):
    doreshka = "upsolved" if s.count("*") > 0 else "solved"
    key_base = "opencup-" if groups_regex.check(s, "1b") else None
    try:
        surnames_ar = get_surnames_ar(s)
    except BaseException as ex:
        raise ex
    surnames = ", ".join(surnames_ar)
    stmt = select(Team).where(Team.surnames == surnames)
    db_team = db.execute(stmt).fetchone()
    if db_team is None:
        raise BaseException(('Failed to process team: "(%s)"' % surnames))
    db_team = db_team[0]
    ids = [db_team.id1, db_team.id2, db_team.id3]
    for id in ids:
        if id == 0:
            continue
        add_results(contestant_scores, id, key_base, doreshka, cnt)


def upd_junior_results(s, db, contestant_scores, cnt):
    # ToDo
    return


def parse_result(row, db, contestant_scores, mode="teams"):
    cnt = 0
    for elem in row[1:]:
        cnt += 1 if elem.count("+") > 0 else 0
    try:
        if mode == "teams":
            upd_team_results(row[0], db, contestant_scores, cnt)
        elif mode == "junior":
            upd_junior_results(row[0], db, contestant_scores, cnt)
    except BaseException as ex:
        print(ex)


def calc_results(contestant_scores, mode="teams", fname_in="standings.csv"):
    db = make_session()
    with open(fname_in, "r") as fin_csv:
        next(fin_csv)
        fin = csv.reader(fin_csv)
        for row in fin:
            parse_result(row, db, contestant_scores, mode=mode)


def save_juniors_results(contestants, fname_out="results.csv"):
    # ToDo
    return


def save_teams_results(contestant_scores, course="1b", fname_out="results.csv"):
    db = make_session()
    with open(fname_out, "w") as fout_csv:
        fout = csv.writer(fout_csv)
        for id, score in contestant_scores.items():
            db_member = db.get(Member, id)
            if not groups_regex.check(db_member.group, course):
                continue
            row = [
                db_member.surname,
                db_member.firstname,
                db_member.middlename,
                db_member.group,
                score["solved"],
                score["upsolved"],
            ]
            fout.writerow(row)
