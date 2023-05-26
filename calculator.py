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


def add_results(contestant_scores, id, key, solved):
    if id not in contestant_scores.keys():
        contestant_scores[id] = dict()
    if key not in contestant_scores[id]:
        contestant_scores[id][key] = 0
    contestant_scores[id][key] += solved


def make_key(s, key_base=None):
    if key_base:
        return key_base
    else:
        return "upsolved" if "*" in s else "solved"


def upd_team_results(s, db, contestant_scores, key_base, cnt):
    key = make_key(s, key_base)
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
        db_member = db.get(Member, id)
        if groups_regex.check(db_member.group, "1b"):
            key = "opencup"
        add_results(contestant_scores, id, key, cnt)


def get_nickname(s):
    return s.replace("* ", "").strip()


def upd_junior_results(s, db, contestant_scores, key_base, cnt):
    key = make_key(s, key_base)
    stmt = select(Member).where(
        Member.nickname == get_nickname(s),
    )
    db_member = db.execute(stmt).fetchone()
    if db_member is None:
        raise BaseException(('Failed to process junior: "%s"' % s))
    db_member = db_member[0]
    add_results(contestant_scores, db_member.id, key, cnt)


def parse_result(
    row, db, contestant_scores, mode="teams", key_base=None, verbose=False
):
    cnt = 0
    for elem in row[1:]:
        cnt += 1 if "+" in elem else 0
    try:
        if mode == "teams":
            upd_team_results(row[0], db, contestant_scores, key_base, cnt)
        elif mode == "junior":
            upd_junior_results(row[0], db, contestant_scores, key_base, cnt)
    except BaseException as ex:
        if verbose:
            print(ex)


def calc_results(
    contestant_scores,
    mode="teams",
    key_base="",
    fname_in="standings.csv",
    verbose=False,
):
    db = make_session()
    with open(fname_in, "r") as fin_csv:
        next(fin_csv)
        fin = csv.reader(fin_csv)
        for row in fin:
            parse_result(
                row,
                db,
                contestant_scores,
                mode=mode,
                key_base=key_base,
                verbose=verbose,
            )


def save_results(
    contestant_scores,
    course="1b",
    key_scores={"solved": 3, "upsolved": 1, "skat": -6},
    fname_out="results.csv",
):
    db = make_session()
    results = []
    for id, score in contestant_scores.items():
        db_member = db.get(Member, id)
        if not groups_regex.check(db_member.group, course):
            continue
        contestant_row = [id]
        contestant_result = 0
        for key, coef in key_scores.items():
            contestant_row.append(score[key] if key in score.keys() else 0)
            contestant_result += contestant_row[-1] * coef
        contestant_row.append(contestant_result)
        results.append((contestant_result, contestant_row))
    results = sorted(results)[::-1]
    with open(fname_out, "w") as fout_csv:
        fout = csv.writer(fout_csv)
        header = (
            ["N", "Фамилия", "Имя", "Отчество", "Группа"]
            + list(key_scores.keys())
            + ["Рейтинг"]
        )
        fout.writerow(header)
        cnt = 1
        for _, contestant in results:
            db_member = db.get(Member, contestant[0])
            row = [
                cnt,
                db_member.surname,
                db_member.firstname,
                db_member.middlename,
                db_member.group,
            ] + contestant[1:]
            cnt += 1
            fout.writerow(row)
