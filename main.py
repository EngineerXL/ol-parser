import sys
import scenarios

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise RuntimeError('Expected an argument, try "bash run.sh help"')
    opt = sys.argv[1]
    if opt == "reg_year" or opt == "reg_summer":
        scenarios.handle_reg(opt[4:])
    elif opt == "mailing":
        scenarios.handle_mailing()
    elif opt == "dump":
        scenarios.handle_dump()
    elif opt == "res_spring" or opt == "res_fall":
        scenarios.handle_term(opt[4:])
    elif opt == "practice_year":
        scenarios.handle_practice()
    elif opt == "practice_summer":
        scenarios.handle_summer()
    elif opt == "help":
        scenarios.print_help()
    else:
        print("Unknown key:", opt)
