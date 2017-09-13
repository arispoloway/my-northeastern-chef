from chef import DiscordDaemon
import shelve
from chef.Configuration import ConfigurationCreator
from chef.ConfigurationSettings import ConfigurationSettings

ConfigurationSettings.initialize_channels()

DiscordDaemon.start_discord_daemon()

