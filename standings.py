from bs4 import BeautifulSoup
import csv
import utils


def parse_html_row(row, mode="teams"):
    elem = row.find("td", class_="contestant-cell")
    contestant = elem.contents[0].strip()
    res = [contestant]
    for task in row.find_all("td", problemid=True):
        status = task.find("span", class_=True)
        res.append(status.contents[0].strip())
    return res


def standings_to_csv(
    url=None, mode="teams", fname_in="standings.html", fname_out="standings.csv"
):
    utils.save_from_url(url, fname_in)
    with open(fname_in, "r") as fin:
        soup = BeautifulSoup(fin, "lxml")
        with open(fname_out, "w") as fout_csv:
            fout = csv.writer(fout_csv)
            table = soup.find("table", class_="standings")
            info_row = ["team-name"]
            for elem in table.find("tr").find_all("span"):
                info_row.append(elem.contents[0])
            fout.writerow(info_row)
            for elem in table.find_all("tr", participantid=True):
                ar = parse_html_row(elem, mode=mode)
                fout.writerow(ar)
