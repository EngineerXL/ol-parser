import calculator
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
        fname_in=DATA_FOLDER + "registration_teams.csv", mode="teams"
    )
    registration.register_pg(
        fname_in=DATA_FOLDER + "registration_junior.csv", mode="junior"
    )
    standings.cf_to_csv(
        url=URL_STANDINGS_JUNIOR,
        fname_out=DATA_FOLDER + "standings_junior.csv",
    )
    standings.cf_to_csv(
        url=URL_STANDINGS_TEAMS,
        fname_out=DATA_FOLDER + "standings_teams.csv",
    )
    standings.ya_to_csv(
        url=URL_RUCODE_CF,
        fname_out=DATA_FOLDER + "standings_rucode_cf.csv",
    )
    standings.ya_to_csv(
        url=URL_RUCODE_AB,
        fname_out=DATA_FOLDER + "standings_rucode_ab.csv",
    )
    contestants = dict()
    calculator.calc_results(
        contestants,
        mode="teams",
        fname_in=DATA_FOLDER + "standings_teams.csv",
        verbose=True,
    )
    calculator.calc_results(
        contestants,
        mode="junior",
        fname_in=DATA_FOLDER + "standings_junior.csv",
        verbose=True,
    )
    calculator.calc_results(
        contestants,
        mode="teams",
        key_base="rucode",
        fname_in=DATA_FOLDER + "standings_rucode_ab.csv",
    )
    calculator.calc_results(
        contestants,
        mode="teams",
        key_base="rucode",
        fname_in=DATA_FOLDER + "standings_rucode_cf.csv",
    )
    calculator.save_results(
        contestants,
        course="1b",
        key_scores={"solved": 3, "upsolved": 1, "skat": -6, "olymp": 6, "opencup": 1},
        fname_out=DATA_FOLDER + "results_1b.csv",
    )
    calculator.save_results(
        contestants,
        course="3b",
        key_scores={"solved": 3, "upsolved": 1, "skat": -6, "rucode": 6},
        fname_out=DATA_FOLDER + "results_3b.csv",
    )
