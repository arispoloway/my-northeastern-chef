from chef import DiscordDaemon
import shelve
from chef.Configuration import ConfigurationCreator
from chef import ConfigurationSettingManager


ConfigurationSettingManager.initialize_channels()

DiscordDaemon.start_discord_daemon()
