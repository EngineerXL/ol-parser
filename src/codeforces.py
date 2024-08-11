from db import *


def print_cf_teams(f):
    pg = make_session()
    for team in pg.execute(text('SELECT * FROM "Teams"')):
        s = " | " + team.login + " | " + team.password + " | " + team.teamname
        f.write(s + "\n")


def print_cf_juniors(f, mode="juniors"):
    pg = make_session()
    for member in pg.execute(text('SELECT * FROM "Members"')):
        if member.login is None:
            continue
        s = " | " + member.login + " | " + member.password + " | " + member.nickname
        f.write(s + "\n")


def print_cf(fname_out="registration.csv", mode="teams"):
    with open(fname_out, "w") as f:
        if mode == "teams":
            print_cf_teams(f)
        elif mode == "juniors" or mode == "summer":
            print_cf_juniors(f, mode)
        else:
            raise RuntimeError("Unknown key: " + mode)
