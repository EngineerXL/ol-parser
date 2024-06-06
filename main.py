import calculator
import codeforces
import db
import groups_regex
import mailing
import registration
import standings
import sys
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
    opt = sys.argv[1]
    if opt == "dump":
        for el in groups_regex.groups.keys():
            db.dump_members(fname_out=DATA_FOLDER + "dump_" + el + ".csv", course=el)
    elif opt == "mailing":
        # ПЕРЕД РАССЫЛКОЙ ПРОВЕРЬ ТЕКСТ ПИСЬМА
        # mailing.send_cf(mode="junior")
        codeforces.print_cf(DATA_FOLDER + "cf_teams.txt", mode="teams")
        codeforces.print_cf(DATA_FOLDER + "cf_juniors.txt", mode="junior")
    elif opt == "summer":
        # Summer practice
        standings.cf_to_csv(
            url=URL_SUMMER_STANDINGS,
            fname_out=DATA_FOLDER + "standings_summer.csv",
        )
        standings.cf_to_csv(
            url=URL_SUMMER_BASE,
            fname_out=DATA_FOLDER + "standings_base.csv",
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_summer.csv",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_summer.csv",
            key_base="visited",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_base.csv",
            key_base="base",
            verbose=True,
        )
    elif opt == "spring":
        contestants = dict()
        # Juniors Spring
        standings.cf_to_csv(
            url=URL_JUNIORS_BASE_SPRING,
            fname_out=DATA_FOLDER + "standings_juniors_base_spring.csv",
        )
        standings.cf_to_csv(
            url=URL_JUNIORS_STANDINGS_SPRING,
            fname_out=DATA_FOLDER + "standings_juniors_spring.csv",
        )
        standings.cf_to_csv(
            url=URL_OLYMP_SPRING,
            fname_out=DATA_FOLDER + "standings_olymp_spring.csv",
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_juniors_spring.csv",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_juniors_base_spring.csv",
            key_base="base",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_olymp_spring.csv",
            key_base="olymp",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "jun_cheaters_spring.csv",
            key_base="cheat",
            verbose=True,
        )

        # Spring teams
        standings.cf_to_csv(
            url=URL_TEAMS_STANDINGS_SPRING,
            fname_out=DATA_FOLDER + "standings_teams_spring.csv",
        )
        calculator.calc_results(
            contestants,
            mode="teams",
            fname_in=DATA_FOLDER + "standings_teams_spring.csv",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="teams",
            fname_in=DATA_FOLDER + "standings_teams_spring.csv",
            key_base="visited",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="teams",
            fname_in=DATA_FOLDER + "standings_olymp_spring.csv",
            key_base="olymp",
            verbose=True,
        )

        # 1b
        calculator.save_results(
            contestants,
            course="1b",
            key_scores={
                "base": 2,
                "solved": 3,
                "upsolved": 1,
                "olymp": 6,
                "opencup-solved": 1,
                "opencup-upsolved": 1,
                "cheat": -806,
            },
            fname_out=DATA_FOLDER + "results_1b.csv",
        )
        # 3b
        calculator.save_results(
            contestants,
            course="3b",
            key_scores={
                "solved": 3,
                "upsolved": 1,
                "visited": 1,
                "olymp": 6,
            },
            fname_out=DATA_FOLDER + "results_3b.csv",
        )
        # 4b
        calculator.save_results(
            contestants,
            course="4b",
            key_scores={"solved": 3, "upsolved": 1, "visited": 1},
            fname_out=DATA_FOLDER + "results_4b.csv",
        )
    elif opt == "practice":
        contestants = dict()
        # Juniors
        standings.cf_to_csv(
            url=URL_JUNIORS_STANDINGS_YEAR,
            fname_out=DATA_FOLDER + "standings_juniors_year.csv",
        )
        standings.cf_to_csv(
            url=URL_JUNIORS_BASE_YEAR,
            fname_out=DATA_FOLDER + "standings_juniors_base_year.csv",
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_juniors_base_year.csv",
            key_base="base",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_juniors_year.csv",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="junior",
            fname_in=DATA_FOLDER + "standings_juniors_year.csv",
            key_base="visited",
            verbose=True,
        )
        # 1b
        calculator.save_results(
            contestants,
            course="1b",
            key_scores={
                "base": 2,
                "solved": 3,
                "upsolved": 1,
                "visited": 1,
            },
            fname_out=DATA_FOLDER + "practice_1b.csv",
        )

        # Teams
        standings.cf_to_csv(
            url=URL_TEAMS_STANDINGS_YEAR,
            fname_out=DATA_FOLDER + "standings_teams_year.csv",
        )
        calculator.calc_results(
            contestants,
            mode="teams",
            fname_in=DATA_FOLDER + "standings_teams_year.csv",
            verbose=True,
        )
        calculator.calc_results(
            contestants,
            mode="teams",
            fname_in=DATA_FOLDER + "standings_teams_year.csv",
            key_base="visited",
            verbose=True,
        )
        # 2b
        calculator.save_results(
            contestants,
            course="2b",
            key_scores={
                "solved": 3,
                "upsolved": 1,
                "visited": 1,
            },
            fname_out=DATA_FOLDER + "practice_2b.csv",
        )
        # 3b
        calculator.save_results(
            contestants,
            course="3b",
            key_scores={
                "solved": 3,
                "upsolved": 1,
                "visited": 1,
            },
            fname_out=DATA_FOLDER + "practice_3b.csv",
        )
