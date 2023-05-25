from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_html_standings(url):
    r = requests.get(url)
    r.encoding = "utf-8"
    return r.text


def cf_to_csv(url=None, prefix="./data/", suffix="teams"):
    fname_out = prefix + "standings_" + suffix + ".csv"
    soup = BeautifulSoup(get_html_standings(url), "lxml")
    table = soup.find("table", class_="standings")
    df = pd.read_html(str(table))[0]
    df = df.drop(["#", "=", "Penalty"], axis="columns")
    df[:-1].to_csv(fname_out, index=False)


# На ЯКе нужно листать страницы, чтобы получить всю таблицу
def ya_to_csv(url=None, prefix="./data/", suffix="teams"):
    fname_out = prefix + "standings_" + suffix + ".csv"
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
