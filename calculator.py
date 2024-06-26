import csv
import groups_regex
import utils

from db import *
from sqlalchemy import select


def make_key(upsolving, key_base=None):
    if key_base:
        if key_base == "olymp":
            return "upsolved" if upsolving else "olymp"
        else:
            return key_base
    else:
        return "upsolved" if upsolving else "solved"


def add_results(contestant_scores, id, upsolving, key_base, solved, flag1b=False):
    key = make_key(upsolving, key_base)
    key_solved_set = (key_base + "-set") if key_base else "solved-set"
    if flag1b:
        key = "opencup-" + key
        key_solved_set = "opencup-" + key_solved_set
    if id not in contestant_scores.keys():
        contestant_scores[id] = dict()
    if key_solved_set not in contestant_scores[id]:
        contestant_scores[id][key_solved_set] = set()
    if key not in contestant_scores[id]:
        contestant_scores[id][key] = 0
    for task in solved:
        if task not in contestant_scores[id][key_solved_set]:
            contestant_scores[id][key_solved_set].add(task)
            contestant_scores[id][key] += 1


def upd_team_results(s, db, contestant_scores, upsolving, key_base, solved):
    try:
        surnames_ar = utils.get_surnames_ar(s)
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
        add_results(
            contestant_scores,
            id,
            upsolving,
            key_base,
            solved,
            groups_regex.check(db_member.group, "1b"),
        )


def get_nickname(s):
    return s.replace("* ", "").strip()


def upd_junior_results(s, db, contestant_scores, upsolving, key_base, solved):
    stmt = select(Member).where(
        Member.nickname == get_nickname(s),
    )
    db_member = db.execute(stmt).fetchone()
    if db_member is None:
        raise BaseException(('Failed to process junior: "%s"' % s))
    db_member = db_member[0]
    # program does not differ 1 course and team solved tasks
    # so it gives strange results
    if not groups_regex.check(db_member.group, "1b"):
        raise BaseException(('Skipping "%s" - not a junior' % s))
    add_results(contestant_scores, db_member.id, upsolving, key_base, solved)


def parse_result(
    header,
    row,
    db,
    contestant_scores,
    mode="teams",
    key_base=None,
    verbose=False,
):
    get_mode = "visiting" if key_base == "visited" else "solving"
    solved = utils.get_solved(header[1:], row[1:], mode=get_mode)
    upsolving = True if "*" in row[0] else False
    try:
        if mode == "teams":
            upd_team_results(row[0], db, contestant_scores, upsolving, key_base, solved)
        elif mode == "juniors":
            upd_junior_results(
                row[0], db, contestant_scores, upsolving, key_base, solved
            )
        else:
            raise RuntimeError("Unknown mode: " + mode)
    except BaseException as ex:
        if verbose:
            print(ex)


def calc_results(
    contestant_scores,
    mode="teams",
    key_base=None,
    fname_in="standings.csv",
    verbose=False,
):
    db = make_session()
    with open(fname_in, "r") as fin_csv:
        fin = csv.reader(fin_csv)
        header = next(fin)
        for row in fin:
            parse_result(
                header,
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
