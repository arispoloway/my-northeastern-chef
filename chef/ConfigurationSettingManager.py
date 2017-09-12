import shelve
from chef.Configuration import ConfigurationCreator


def get_configuration_listing():
    return shelve.open("configuration-listing")


def initialize_channels():
    channels = []
    for item in get_configuration_listing():
        config = shelve.open(item)

        channel = ConfigurationCreator.create_configuration_from_settings(config)
        channels.append(channel)

    return channels
