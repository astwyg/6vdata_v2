import sys, os, json, platform

with open(os.path.join(os.path.abspath(__file__),"..",'conf.json'),"r") as f:
    config = json.loads(f.read())


def get_conf(conf_name, conf_type=None):
    return config.get(conf_name)

def get_env():
    '''
    windows视为debug, linux视为product
    :return: 
    '''
    if 'Windows' in platform.system():
        return "debug"
    else:
        return "product"
