from chef.Query import ConfigurationCreationQuery
from chef.configuration.DiscordConfiguration import DiscordConfiguration


class ConfigurationCreator(object):

    @staticmethod
    def start_configuration_from_settings(settings):
        if settings.get("configuration-type") == DiscordConfiguration.get_configuration_type():
            configuration = DiscordConfiguration(settings)
        else:
            raise Exception("Invalid channel configuration")
        return configuration

    @staticmethod
    def create_configuration_from_settings(settings):
        configuration = ConfigurationCreator.start_configuration_from_settings(settings)
        ConfigurationCreationQuery().apply(configuration)