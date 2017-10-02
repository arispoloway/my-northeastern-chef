import os
import shelve
import sys

from chef.configuration.ConfigurationCreator import ConfigurationCreator

base_setting_path = os.path.dirname(os.path.abspath(sys.argv[0]))+ "/configuration_settings/"
if not os.path.exists(base_setting_path):
    os.makedirs(base_setting_path)


class ConfigurationSettings(object):

    configuration_listing = shelve.open(base_setting_path + "configuration_listing")

    @staticmethod
    def get_configuration_listing():
        if "listing" not in ConfigurationSettings.configuration_listing:
            ConfigurationSettings.configuration_listing["listing"] = []
        return ConfigurationSettings.configuration_listing["listing"]

    @staticmethod
    def open_settings(configuration_type: str, filename: str):
        directory = base_setting_path + configuration_type + "/"
        return ConfigurationSettings(shelve.open(directory + filename))


    @staticmethod
    def create_new_settings(configuration_type: str, filename: str):
        directory = base_setting_path + configuration_type + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        s = ConfigurationSettings.open_settings(configuration_type, filename)
        s.set("configuration-type", configuration_type)
        s.set("school", "")

        ConfigurationSettings.add_to_configuration_listing(configuration_type, filename)

        return s

    @staticmethod
    def add_to_configuration_listing(configuration_type: str, name: str):
        if "listing" not in ConfigurationSettings.configuration_listing:
            ConfigurationSettings.configuration_listing["listing"] = []
        ConfigurationSettings.configuration_listing["listing"] = ConfigurationSettings.configuration_listing["listing"] + [{"configuration-type": configuration_type, "name": name}]
        ConfigurationSettings.configuration_listing.sync()

    @staticmethod
    def initialize_channels():
        channels = []
        for item in ConfigurationSettings.get_configuration_listing():
            settings = ConfigurationSettings.open_settings(item["configuration-type"], item["name"])

            channel = ConfigurationCreator.start_configuration_from_settings(settings)
            channels.append(channel)

        return channels

    def __init__(self, settings):
        self.shelve = settings

    def set(self, key, value):
        self.shelve[key] = value
        self.shelve.sync()

    def get(self, key):
        return self.shelve[key]

    def has_key(self, key):
        return key in self.shelve





