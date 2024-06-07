import calculator
import codeforces
import groups_regex
import mailing
import registration
import standings
import utils

from cfg_parser import config


DATA_FOLDER = "./data/"
DOWNLOAD = True
EXT = ".csv"


def handle_reg():
    if DOWNLOAD:
        utils.save_from_url(
            config["url_reg_junior"], DATA_FOLDER + "registration_junior.csv"
        )
        utils.save_from_url(config["url_reg_teams"] + "registration_teams.csv")
    registration.register_pg(
        fname_in=DATA_FOLDER + "registration_junior.csv", mode="junior"
    )
    registration.register_pg(
        fname_in=DATA_FOLDER + "registration_teams.csv", mode="teams"
    )


def handle_dump():
    for el in groups_regex.groups.keys():
        db.dump_members(fname_out=DATA_FOLDER + "dump_" + el + ".csv", course=el)


def handle_mailing():
    # ПЕРЕД РАССЫЛКОЙ ПРОВЕРЬ ТЕКСТ ПИСЬМА
    # mailing.send_cf(mode="junior")
    codeforces.print_cf(DATA_FOLDER + "cf_teams.txt", mode="teams")
    codeforces.print_cf(DATA_FOLDER + "cf_juniors.txt", mode="junior")


def download_tables(todo, verbose=True):
    for url, val in todo.items():
        fname = DATA_FOLDER + val[1]
        if val[0] == "cf":
            standings.cf_to_csv(url=url, fname_out=fname)
        elif val[0] == "ya":
            standings.ya_to_csv(url=url, fname_out=fname)
        elif val[0] == "ti":
            standings.ti_to_csv(url=url, fname_out=fname)
        else:
            print("Unknown table type:", val[0])


def process_tables(contestants, todo, mode="junior", verbose=True):
    for key_base, fname in todo.items():
        calculator.calc_results(
            contestants,
            mode=mode,
            fname_in=DATA_FOLDER + fname,
            key_base=key_base,
            verbose=verbose,
        )


def save_results(contestants, todo):
    for course, val in todo.items():
        calculator.save_results(
            contestants,
            course=course,
            key_scores=val[1],
            fname_out=DATA_FOLDER + val[0],
        )


# Summer practice
def handle_summer():
    if DOWNLOAD:
        download_tables(
            {
                config["url_summer_base"]: ("cf", "standings_summer_base.csv"),
                config["url_summer_standings"]: ("cf", "standings_summer.csv"),
            },
        )
    contestants = dict()
    process_tables(
        contestants,
        {
            "base": "standings_summer_base.csv",
            None: "standings_summer.csv",
            "visited": "standings_summer.csv",
        },
        mode="junior",
        verbose=True,
    )
    save_results(
        contestants,
        {
            "1b": (
                "summer_practice_1b.csv",
                {
                    "base": 2,
                    "solved": 3,
                    "upsolved": 1,
                    "visited": 1,
                },
            )
        },
    )


# fall/spring
def handle_term(term):
    if DOWNLOAD:
        download_tables(
            {
                config["url_juniors_base_" + term]: (
                    "cf",
                    "standings_juniors_base_" + term + EXT,
                ),
                config["url_juniors_standings_" + term]: (
                    "cf",
                    "standings_juniors_" + term + EXT,
                ),
                config["url_olymp_" + term]: (
                    "cf",
                    "standings_olymp_" + term + EXT,
                ),
                config["url_teams_standings_" + term]: (
                    "cf",
                    "standings_teams_" + term + EXT,
                ),
            }
        )
    contestants = dict()
    # Juniors
    process_tables(
        contestants,
        {
            "base": "standings_juniors_base_" + term + EXT,
            None: "standings_juniors_" + term + EXT,
            "olymp": "standings_olymp_" + term + EXT,
            "cheat": "jun_cheaters_" + term + EXT,
        },
        mode="junior",
        verbose=True,
    )
    # Teams
    process_tables(
        contestants,
        {
            None: "standings_teams_" + term + EXT,
            "visited": "standings_teams_" + term + EXT,
            "olymp": "standings_olymp_" + term + EXT,
        },
        mode="teams",
        verbose=True,
    )
    save_results(
        contestants,
        {
            "1b": (
                "results_1b_" + term + EXT,
                {
                    "base": 2,
                    "solved": 3,
                    "upsolved": 1,
                    "olymp": 6,
                    "opencup-solved": 1,
                    "opencup-upsolved": 1,
                    "cheat": -806,
                },
            ),
            "3b": (
                "results_3b_" + term + EXT,
                {
                    "solved": 3,
                    "upsolved": 1,
                    "visited": 1,
                    "olymp": 6,
                },
            ),
            "4b": (
                "results_4b_" + term + EXT,
                {"solved": 3, "upsolved": 1, "visited": 1},
            ),
        },
    )


# Year practice
def handle_practice():
    if DOWNLOAD:
        download_tables(
            {
                config["url_juniors_standings_year"]: (
                    "cf",
                    "standings_juniors_year.csv",
                ),
                config["url_juniors_base_year"]: (
                    "cf",
                    "standings_juniors_base_year.csv",
                ),
                config["url_teams_standings_year"]: (
                    "cf",
                    "standings_teams_year.csv",
                ),
            }
        )
    contestants = dict()
    # Juniors
    process_tables(
        contestants,
        {
            "base": "standings_juniors_base_year.csv",
            None: "standings_juniors_year.csv",
            "visited": "standings_juniors_year.csv",
        },
        mode="junior",
        verbose=True,
    )
    # Teams
    process_tables(
        contestants,
        {
            None: "standings_teams_year.csv",
            "visited": "standings_teams_year.csv",
        },
        mode="teams",
        verbose=True,
    )
    save_results(
        contestants,
        {
            "1b": (
                "practice_1b.csv",
                {
                    "base": 2,
                    "solved": 3,
                    "upsolved": 1,
                    "visited": 1,
                },
            ),
            "2b": (
                "practice_2b.csv",
                {
                    "solved": 3,
                    "upsolved": 1,
                    "visited": 1,
                },
            ),
            "3b": (
                "practice_3b.csv",
                {
                    "solved": 3,
                    "upsolved": 1,
                    "visited": 1,
                },
            ),
        },
    )
