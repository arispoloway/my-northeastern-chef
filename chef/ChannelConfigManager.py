import shelve
from chef.Configuration import ConfigurationCreator


def get_channel_listing():
    return shelve.open("channel-listing")


def initialize_channels():
    channels = []
    for item in get_channel_listing():
        config = shelve.open(item)

        channel = ConfigurationCreator.create_channel_from_config(config)
        channels.append(channel)

    return channels
