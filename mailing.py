from email.message import EmailMessage
import time
import smtplib

from cfg_parser import config
from db import *


def gen_msg(member):
    res = ""
    res += "Здравствуйте, %s!\n" % member.nickname
    res += "\n"
    res += "Ваши данные от тестирующей системы:\n"
    res += "Логин: %s\n" % member.login
    res += "Пароль: %s\n" % member.password
    res += "Ссылка на тестирующую систему: " + config["url_cf_junior"] + "\n"
    res += "Чат в Telegram: " + config["url_tg_junior"] + "\n"
    res += "\n"
    res += "С уважением, Максим Инютин\n"
    return res


def send_mail(smtp_server, member, verbose=True):
    msg = EmailMessage()
    msg.set_content(gen_msg(member))
    msg["Subject"] = "Доступ на Codeforces"
    msg["From"] = config["mail"]
    # msg["To"] = ", ".join(emails.split(";"))
    msg["To"] = member.email
    smtp_server.send_message(msg)
    if verbose:
        print("Отправлено письмо", member.nickname, member.email)
    time.sleep(5)


def send_cf_teams(smtp_server, verbose=True):
    pg = make_session()
    cursor = pg.execute(text('SELECT * FROM "Teams"')).all()
    for team in cursor:
        print(team.teamname)


def send_cf_junior(smtp_server, verbose=True):
    pg = make_session()
    cursor = pg.execute(text('SELECT * FROM "Members"')).all()
    for member in cursor:
        if member.mail_sent or member.login is None:
            continue
        send_mail(smtp_server, member, verbose=verbose)
        db_member = pg.get(Member, member.id)
        db_member.mail_sent = True
        pg.commit()


def send_cf(mode="teams", verbose=True):
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(config["mail"], config["mail_password"])
    if mode == "teams":
        send_cf_teams(smtp_server, verbose=verbose)
    elif mode == "junior":
        send_cf_junior(smtp_server, verbose=verbose)
    smtp_server.quit()
