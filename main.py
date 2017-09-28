import threading
import settings
from chef import DiscordDaemon
from chef.Scheduler import Scheduler
from chef.configuration.ConfigurationSettings import ConfigurationSettings


ConfigurationSettings.initialize_channels()
Scheduler.initialize()


def launch_daemon_thread(func, args):
    t = threading.Thread(target=func, args=args)
    t.daemon = True
    t.start()
    return t


launch_daemon_thread(DiscordDaemon.start_discord_daemon, (settings.discord_token,))

Scheduler.run()
