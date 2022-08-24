import configparser
import os

def read(name):
    config = configparser.ConfigParser()
    if name is None:
        name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default.ini')
    config.read(name)
    return config



