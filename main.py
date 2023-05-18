import calculator
import registration
import standings
import utils

DATA_FOLDER = "./data/"
DOWNLOAD = True

if __name__ == "__main__":
    if DOWNLOAD:
        utils.save_from_url(URL_REG_JUNIOR, DATA_FOLDER + "registration_junior.csv")
        utils.save_from_url(URL_REG_TEAMS, DATA_FOLDER + "registration_teams.csv")
        utils.save_from_url(URL_STANDINGS_JUNIOR, DATA_FOLDER + "standings_junior.html")
        utils.save_from_url(URL_STANDINGS_TEAMS, DATA_FOLDER + "standings_teams.html")
    registration.register_pg(
        fname_in=DATA_FOLDER + "registration_teams.csv", mode="teams"
    )
    registration.register_pg(
        fname_in=DATA_FOLDER + "registration_junior.csv", mode="junior"
    )
    standings.standings_to_csv(
        fname_in=DATA_FOLDER + "standings_teams.html",
        fname_out=DATA_FOLDER + "standings_teams.csv",
    )
    standings.standings_to_csv(
        fname_in=DATA_FOLDER + "standings_junior.html",
        fname_out=DATA_FOLDER + "standings_junior.csv",
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
