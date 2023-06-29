from db import *


def print_cf(fname_out="registration.csv", mode="teams"):
    pg = make_session()
    if mode == "junior":
        with open(fname_out, "w") as f:
            for member in pg.execute('SELECT * FROM "Members"'):
                s = (
                    " | "
                    + member.login
                    + " | "
                    + member.password
                    + " | "
                    + member.nickname
                )
                f.write(s + "\n")
