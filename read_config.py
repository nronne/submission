import configparser

def read(name):
    config = configparser.ConfigParser()
    if name is None:
        name = 'default.ini'
    config.read(name)
    return config



