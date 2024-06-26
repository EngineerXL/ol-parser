from email.message import EmailMessage
import time
import smtplib

from cfg_parser import config
from db import *


def gen_msg(nickname, login, password, cf_link, tg_link):
    res = ""
    res += "Здравствуйте, %s!\n" % nickname
    res += "\n"
    res += "Ваши данные от тестирующей системы:\n"
    res += "Логин: %s\n" % login
    res += "Пароль: %s\n" % password
    res += "Ссылка на тестирующую систему: " + cf_link + "\n"
    res += "Чат в Telegram: " + tg_link + "\n"
    res += "\n"
    res += "С уважением, Максим Инютин\n"
    return res


def send_mail(
    smtp_server, emails, nickname, login, password, cf_link, tg_link, verbose=True
):
    msg = EmailMessage()
    msg.set_content(gen_msg(nickname, login, password, cf_link, tg_link))
    msg["Subject"] = "Доступ на Codeforces"
    msg["From"] = config["mail"]
    msg["To"] = ", ".join(emails)
    # smtp_server.send_message(msg)
    if verbose:
        print("Отправлено письмо", emails, nickname)
    # time.sleep(5)


def send_cf_teams(smtp_server, verbose=True):
    pg = make_session()
    cursor = pg.execute(text('SELECT * FROM "Teams"')).all()
    for team in cursor:
        if team.mail_sent:
            continue
        emails = []
        for member in [
            pg.get(Member, team.id1),
            pg.get(Member, team.id2),
            pg.get(Member, team.id3),
        ]:
            if member is not None and member.email != "":
                emails.append(member.email)
        if len(emails) == 0:
            print(team.teamname, "does not have any emails!")
            continue
        send_mail(
            smtp_server,
            emails,
            team.teamname,
            team.login,
            team.password,
            config["url_cf_teams"],
            config["url_tg_teams"],
            verbose=verbose,
        )
        db_team = pg.get(Team, team.id)
        db_team.mail_sent = True
        pg.commit()


def send_cf_juniors(smtp_server, mode="juniors", verbose=True):
    pg = make_session()
    cursor = pg.execute(text('SELECT * FROM "Members"')).all()
    for member in cursor:
        if member.mail_sent or member.login is None:
            continue
        send_mail(
            smtp_server,
            [member.email],
            member.nickname,
            member.login,
            member.password,
            config["url_cf_" + mode],
            config["url_tg_" + mode],
            verbose=verbose,
        )
        db_member = pg.get(Member, member.id)
        db_member.mail_sent = True
        pg.commit()


def send_cf(smtp_server, mode="teams", verbose=True):
    if mode == "teams":
        send_cf_teams(smtp_server, verbose=verbose)
    elif mode == "juniors" or mode == "summer":
        send_cf_juniors(smtp_server, mode, verbose=verbose)
    else:
        raise RuntimeError("Unknowm mode: " + mode)


def handle_mailing(mode="teams", verbose=True):
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(config["mail"], config["mail_password"])
    send_cf(smtp_server, mode, verbose=verbose)
    smtp_server.quit()
