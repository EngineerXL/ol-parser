import calculator
import registration
import standings
import utils

URL_STANDINGS_TEAMS = (
    "https://codeforces.com/spectator/ranklist/053d4ae7c01d798cb3c34dc6327a5aa7"
)
URL_STANDINGS_JUNIOR = (
    "https://codeforces.com/spectator/ranklist/688ae72c8604c282ed911633e34d7f55"
)
URL_RUCODE_CF = (
    "https://official.contest.yandex.ru/rucode6.5/contest/48589/standings/?p="
)

URL_RUCODE_AB = (
    "https://official.contest.yandex.ru/rucode6.5/contest/48590/standings/?p="
)

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
        prefix=DATA_FOLDER,
        suffix="junior",
    )
    standings.cf_to_csv(
        url=URL_STANDINGS_TEAMS,
        prefix=DATA_FOLDER,
        suffix="teams",
    )
    standings.ya_to_csv(
        url=URL_RUCODE_CF,
        prefix=DATA_FOLDER,
        suffix="rucode_cf",
    )
    standings.ya_to_csv(
        url=URL_RUCODE_AB,
        prefix=DATA_FOLDER,
        suffix="rucode_ab",
    )
    contestants = dict()
    calculator.calc_results(
        contestants,
        mode="teams",
        fname_in=DATA_FOLDER + "standings_teams.csv",
    )
    calculator.calc_results(
        contestants,
        mode="junior",
        fname_in=DATA_FOLDER + "standings_junior.csv",
    )
    calculator.save_juniors_results(
        contestants,
        fname_out=DATA_FOLDER + "results_juniors.csv",
    )
    calculator.save_teams_results(
        contestants,
        course="2b",
        fname_out=DATA_FOLDER + "results_2b.csv",
    )
    calculator.save_teams_results(
        contestants,
        course="3b",
        fname_out=DATA_FOLDER + "results_3b.csv",
    )
    calculator.save_teams_results(
        contestants,
        course="4b",
        fname_out=DATA_FOLDER + "results_4b.csv",
    )
    calculator.save_teams_results(
        contestants,
        course="1m",
        fname_out=DATA_FOLDER + "results_1m.csv",
    )
    calculator.save_teams_results(
        contestants,
        course="2m",
        fname_out=DATA_FOLDER + "results_2m.csv",
    )
