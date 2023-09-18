import calculator
import codeforces
import db
import groups_regex
import mailing
import registration
import standings
import utils

from urls import *

DATA_FOLDER = "./data/"
DOWNLOAD = True

if __name__ == "__main__":
    if DOWNLOAD:
        utils.save_from_url(URL_REG_JUNIOR, DATA_FOLDER + "registration_junior.csv")
        utils.save_from_url(URL_REG_TEAMS, DATA_FOLDER + "registration_teams.csv")
    registration.register_pg(
        fname_in=DATA_FOLDER + "registration_junior.csv", mode="junior"
    )
    registration.register_pg(
        fname_in=DATA_FOLDER + "registration_teams.csv", mode="teams"
    )
    for el in groups_regex.groups.keys():
        db.dump_members(fname_out=DATA_FOLDER + "dump_" + el + ".csv", course=el)
    # ПЕРЕД РАССЫЛКОЙ ПРОВЕРЬ ТЕКСТ ПИСЬМА
    # mailing.send_cf(mode="junior")
    codeforces.print_cf(DATA_FOLDER + "cf_teams.txt", mode="teams")
    codeforces.print_cf(DATA_FOLDER + "cf_juniors.txt", mode="junior")

    # standings.cf_to_csv(
    #     url=URL_SUMMER_STANDINGS,
    #     fname_out=DATA_FOLDER + "standings_summer.csv",
    # )
    # standings.cf_to_csv(
    #     url=URL_SUMMER_BASE,
    #     fname_out=DATA_FOLDER + "standings_base.csv",
    # )
    # contestants = dict()
    # calculator.calc_results(
    #     contestants,
    #     mode="junior",
    #     fname_in=DATA_FOLDER + "standings_summer.csv",
    #     verbose=True,
    # )
    # calculator.calc_results(
    #     contestants,
    #     mode="junior",
    #     fname_in=DATA_FOLDER + "standings_summer.csv",
    #     key_base="visited",
    #     verbose=True,
    # )
    # calculator.calc_results(
    #     contestants,
    #     mode="junior",
    #     fname_in=DATA_FOLDER + "standings_base.csv",
    #     key_base="base",
    #     verbose=True,
    # )
    # calculator.save_results(
    #     contestants,
    #     course="1b",
    #     key_scores={"base": 2, "solved": 3, "upsolved": 1, "visited": 1},
    #     fname_out=DATA_FOLDER + "results_1b.csv",
    # )
