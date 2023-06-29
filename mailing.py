from email.message import EmailMessage
import time
import smtplib

from db import *
from my_mail import *


def gen_msg(member):
    res = ""
    res += "Здравствуйте, %s!\n" % member.nickname
    res += "\n"
    res += "Ваши данные от тестирующей системы:\n"
    res += "Логин: %s\n" % member.login
    res += "Пароль: %s\n" % member.password
    res += (
        "Ссылка на тестирующую систему: https://mai2023summer.contest.codeforces.com\n"
    )
    res += "Чат в Telegram: https://t.me/+WgX-vRg9om4zZjJi\n"
    res += "\n"
    res += "С уважением, Максим Инютин\n"
    return res


def send_mail(smtp_server, member, verbose=True):
    msg = EmailMessage()
    msg.set_content(gen_msg(member))
    msg["Subject"] = "Доступ на Codeforces"
    msg["From"] = my_email
    # msg["To"] = ", ".join(emails.split(";"))
    msg["To"] = member.email
    smtp_server.send_message(msg)
    if verbose:
        print("Отправлено письмо", member.nickname, member.email)
    time.sleep(5)


def send_cf(mode="teams", verbose=True):
    pg = make_session()
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(my_email, my_pass)
    if mode == "junior":
        cursor = pg.execute('SELECT * FROM "Members"').all()
        for member in cursor:
            if member.mail_sent:
                continue
            send_mail(smtp_server, member, verbose=verbose)
            db_member = pg.get(Member, member.id)
            db_member.mail_sent = True
            pg.commit()
    smtp_server.quit()
