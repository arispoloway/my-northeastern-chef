import shelve
from chef.Configuration import ConfigurationCreator
import sys
import os


base_setting_path = os.path.dirname(os.path.abspath(sys.argv[0]))+ "/configuration/"
if not os.path.exists(base_setting_path):
    os.makedirs(base_setting_path)



configuration_listing = shelve.open(base_setting_path + "configuration_listing")
if "listing" not in configuration_listing:
    configuration_listing["listing"] = []

def get_configuration_listing():
    return configuration_listing["listing"]

def add_to_configuration_listing(configuration_type : str, name : str):
    configuration_listing["listing"].append({"configuration-type":configuration_type, "name": name})
    print(configuration_listing["listing"])


def initialize_channels():
    channels = []
    for item in get_configuration_listing():
        settings = open_settings(item["configuration-type"], item["name"])

        channel = ConfigurationCreator.create_configuration_from_settings(settings)
        channels.append(channel)

    return channels


def open_settings(configuration_type : str, filename : str):
    directory = base_setting_path + configuration_type + "/"
    return shelve.open(directory + filename)

def create_new_settings(configuration_type : str, filename : str):
    directory = base_setting_path + configuration_type + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    s = open_settings(configuration_type, filename)
    s["configuration-type"] = configuration_type

    add_to_configuration_listing(configuration_type, filename)

    return s
