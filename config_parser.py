#!/usr/bin/python

#
# Config = ConfigParser.ConfigParser()
# Config
# Config.read("server.conf")

import ConfigParser

def ReadParameters(file):
    global Config
    Config = ConfigParser.ConfigParser()
    Config.read(file)
    return ConfigSectionMap("server")

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
