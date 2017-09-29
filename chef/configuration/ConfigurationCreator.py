from chef.Query import ConfigurationCreationQuery

import chef.configuration.DiscordConfiguration
import chef.configuration.MessengerConfiguration



class ConfigurationCreator(object):

    @staticmethod
    def start_configuration_from_settings(settings):
        if settings.get("configuration-type") == chef.configuration.DiscordConfiguration.DiscordConfiguration.get_configuration_type():
            configuration = chef.configuration.DiscordConfiguration.DiscordConfiguration(settings)
        elif settings.get("configuration-type") == chef.configuration.MessengerConfiguration.MessengerConfiguration.get_configuration_type():
            configuration = chef.configuration.MessengerConfiguration.MessengerConfiguration(settings)
        else:
            raise Exception("Invalid channel configuration")
        return configuration

    @staticmethod
    def create_configuration_from_settings(settings):
        configuration = ConfigurationCreator.start_configuration_from_settings(settings)
        ConfigurationCreationQuery().apply(configuration)