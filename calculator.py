import csv

from db import *
from sqlalchemy import select


def get_surnames_ar(s):
    pos = s.find("(")
    if pos == -1:
        raise BaseException(('Could not resolve team name: "%s"' % s))
    ar = s[pos + 1 : -1].replace(",", "")
    return sorted(ar.split())


def read_results(fname_in="standings.csv"):
    contestant_scores = dict()
    with open(fname_in, "r") as fin_csv:
        next(fin_csv)
        fin = csv.reader(fin_csv)
        for row in fin:
            try:
                surnames_ar = get_surnames_ar(row[0])
            except BaseException as ex:
                print(ex)
                continue
            doreshka = "upsolved" if row[0].count("*") > 0 else "solved"
            cnt = 0
            for elem in row[1:]:
                cnt += 1 if elem.count("+") > 0 else 0
            surnames = ", ".join(surnames_ar)
            if surnames not in contestant_scores.keys():
                contestant_scores[surnames] = {
                    "solved": 0,
                    "upsolved": 0,
                }
            contestant_scores[surnames][doreshka] = cnt
    return contestant_scores


def results_to_csv(db, mode="teams", fname_in="standings.csv", fname_out="results.csv"):
    contestant_scores = read_results()
    with open(fname_out, "w") as fout_csv:
        fout = csv.writer(fout_csv)
        # for elem in db.execute('SELECT * FROM "Teams"').fetchall():
        #     print(elem.surnames)
        for surnames, score in contestant_scores.items():
            stmt = select(Team).where(Team.surnames == surnames)
            db_team = db.execute(stmt).fetchone()
            if db_team is None:
                print(('Failed to process team: "(%s)"' % surnames))
                continue
            db_team = db_team[0]
            ids = [db_team.id1, db_team.id2, db_team.id3]
            for elem in ids:
                if elem == 0:
                    continue
                db_member = db.get(Member, elem)
                row = [
                    db_member.surname,
                    db_member.firstname,
                    db_member.middlename,
                    db_member.group,
                    score["solved"],
                    score["upsolved"],
                ]
                fout.writerow(row)
