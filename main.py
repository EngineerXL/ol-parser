import calculator
import registration
import standings

STANDINGS_URL = None
MODE = "teams"

REGISTRATION_URL = None

if __name__ == "__main__":
    registration.register_to_csv(url=REGISTRATION_URL, mode=MODE)
    registration.register_pg(mode=MODE)
    standings.standings_to_csv(url=STANDINGS_URL, mode=MODE)
    calculator.results_to_csv(registration.make_session(), mode=MODE)
