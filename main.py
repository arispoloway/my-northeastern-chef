import settings
from chef import DiscordDaemon
from chef.configuration.ConfigurationSettings import ConfigurationSettings

ConfigurationSettings.initialize_channels()

DiscordDaemon.start_discord_daemon(settings.discord_token)

