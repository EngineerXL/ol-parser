import sys
import scenarios

if __name__ == "__main__":
    scenarios.handle_reg()
    opt = sys.argv[1]
    if opt == "dump":
        scenarios.handle_dump()
    elif opt == "mailing":
        scenarios.handle_mailing()
    elif opt == "summer":
        scenarios.handle_summer()
    elif opt == "spring" or opt == "fall":
        scenarios.handle_term(opt)
    elif opt == "practice":
        scenarios.handle_practice()
    else:
        print("Unknown key:", opt)
