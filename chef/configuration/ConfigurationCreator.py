from chef.Query import ConfigurationCreationQuery




class ConfigurationCreator(object):

    @staticmethod
    def start_configuration_from_settings(settings):
        from chef.configuration.DiscordConfiguration import DiscordConfiguration
        from chef.configuration.MessengerConfiguration import MessengerConfiguration

        if settings.get("configuration-type") == DiscordConfiguration.get_configuration_type():
            configuration = DiscordConfiguration(settings)
        elif settings.get("configuration-type") == MessengerConfiguration.get_configuration_type():
            configuration = MessengerConfiguration(settings)
        else:
            raise Exception("Invalid channel configuration")
        return configuration

    @staticmethod
    def create_configuration_from_settings(settings):
        configuration = ConfigurationCreator.start_configuration_from_settings(settings)
        ConfigurationCreationQuery().apply(configuration)