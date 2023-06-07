from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_html_standings(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    return r.text


# Таблица объединяет все контесты, поэтому надо шаманить с именами столбцов
def cf_to_csv(url, fname_out="./data/standings_teams.csv"):
    soup = BeautifulSoup(get_html_standings(url), "lxml")
    table = soup.find("table", class_="standings")
    df = pd.read_html(str(table))[0]
    df = df.drop(["#", "=", "Penalty"], axis="columns")
    for i in range(26):
        c = chr(ord("A") + i)
        df = df.rename(columns={c: c + ".0"})
    cols = list(df.columns)
    contest_cnt = 0
    raname_dct, contest = dict(), dict()
    prev_c = "Z"
    for el in cols[1:]:
        c = el[0]
        if c < prev_c:
            contest = {chr(ord("A") + i): 0 for i in range(26)}
            contest_cnt += 1
        prev_c = c
        contest[c] += 1
        raname_dct[el] = c + str(contest[c]) + "." + str(contest_cnt)
    df.rename(columns=raname_dct, inplace=True)
    df[:-1].to_csv(fname_out, index=False)


# На ЯКе нужно листать страницы, чтобы получить всю таблицу
def ya_to_csv(url, fname_out="./data/standings_teams.csv"):
    i = 1
    df = pd.DataFrame()
    while True:
        soup = BeautifulSoup(get_html_standings(url + str(i)), "lxml")
        table = soup.find("table", class_="table")
        if table == None:
            df = df.drop(["№", "Очки", "Штраф"], axis="columns")
            df.to_csv(fname_out, index=False)
            return
        df = pd.concat([df, pd.read_html(str(table))[0]])
        i += 1


def ti_to_csv(url, fname_out="./data/standings_teams.csv"):
    soup = BeautifulSoup(get_html_standings(url), "lxml")
    table = soup.find("table", class_="monitor")
    df = pd.read_html(str(table))[0]
    df = df.drop(["Rank", "Solved", "Time"], axis="columns")
    df[:-2].to_csv(fname_out, index=False)
