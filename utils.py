import requests


def save_from_url(url=None, fname=None):
    if url and fname:
        r = requests.get(url)
        r.encoding = "utf-8"
        with open(fname, "w") as fout:
            fout.write(r.text)
