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
        url=URL_STANDINGS_JUN_OL,
        fname_out=DATA_FOLDER + "standings_jun_ol.csv",
    )
    standings.cf_to_csv(
        url=URL_STANDINGS_TEAMS,
        fname_out=DATA_FOLDER + "standings_teams.csv",
    )
    standings.ti_to_csv(
        url=URL_URAL_DIV2,
        fname_out=DATA_FOLDER + "standings_ural2.csv",
    )
    standings.ti_to_csv(
        url=URL_URAL_DIV1,
        fname_out=DATA_FOLDER + "standings_ural1.csv",
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
        mode="junior",
        key_base="olymp",
        fname_in=DATA_FOLDER + "standings_jun_ol.csv",
        verbose=True,
    )
    calculator.calc_results(
        contestants,
        mode="teams",
        key_base="ural",
        fname_in=DATA_FOLDER + "standings_ural1.csv",
    )
    calculator.calc_results(
        contestants,
        mode="teams",
        key_base="ural",
        fname_in=DATA_FOLDER + "standings_ural2.csv",
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
    calculator.calc_results(
        contestants,
        mode="teams",
        key_base="cheat",
        fname_in=DATA_FOLDER + "cheaters.csv",
        verbose=True,
    )
    calculator.save_results(
        contestants,
        course="1b",
        key_scores={"solved": 3, "upsolved": 1, "olymp": 6, "opencup": 1},
        fname_out=DATA_FOLDER + "results_1b.csv",
    )
    calculator.save_results(
        contestants,
        course="3b",
        key_scores={"solved": 3, "upsolved": 1, "cheat": -10, "ural": 6, "rucode": 6},
        fname_out=DATA_FOLDER + "results_3b.csv",
    )
