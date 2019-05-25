import sys, os, json

with open(os.path.join(os.path.abspath(__file__),'..','conf.json'),"r") as f:
    config = json.loads(f.read())


def get_conf(conf_name, conf_type=None):
    return config.get(conf_name)
