import calculator
import codeforces
import db
import mailing
import registration
import standings
import utils

from urls import *

DATA_FOLDER = "./data/"
DOWNLOAD = True

if __name__ == "__main__":
    if DOWNLOAD:
        utils.save_from_url(URL_REG_SUMMER, DATA_FOLDER + "registration_summer.csv")
    registration.register_pg(
        fname_in=DATA_FOLDER + "registration_summer.csv", mode="junior"
    )
    mailing.send_cf(mode="junior")
    codeforces.print_cf(DATA_FOLDER + "cf.txt", mode="junior")
    # db.print_members(course="1b")

    # standings.cf_to_csv(
    #     url=URL_STANDINGS_JUNIOR,
    #     fname_out=DATA_FOLDER + "standings_junior.csv",
    # )
    # contestants = dict()
    # calculator.calc_results(
    #     contestants,
    #     mode="junior",
    #     fname_in=DATA_FOLDER + "standings_junior.csv",
    #     verbose=True,
    # )
    # calculator.save_results(
    #     contestants,
    #     course="1b",
    #     key_scores={"solved": 3, "upsolved": 1, "visited": 1},
    #     fname_out=DATA_FOLDER + "results_1b.csv",
    # )
