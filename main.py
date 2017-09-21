from chef import DiscordDaemon
from chef.ConfigurationSettings import ConfigurationSettings
import settings


ConfigurationSettings.initialize_channels()

DiscordDaemon.start_discord_daemon(settings.discord_token)

