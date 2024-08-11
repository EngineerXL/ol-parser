import json


def load_cfg(fname):
    with open(fname, "r") as cfg_file:
        return json.load(cfg_file)


config = load_cfg("cfg/config.json")
