import threading
import settings

from chef import MessengerDaemon, DiscordDaemon

from chef.Scheduler import Scheduler
from chef.configuration.ConfigurationSettings import ConfigurationSettings
import asyncio


ConfigurationSettings.initialize_channels()
Scheduler.initialize()


def asyncio_wrapper_thread(event_loop, func, args):
    asyncio.set_event_loop(event_loop)
    func(*args)


def launch_daemon_thread(func, args):
    t = threading.Thread(target=asyncio_wrapper_thread, args=(asyncio.get_event_loop(), func) + (args,))
    t.daemon = True
    t.start()
    return t


launch_daemon_thread(DiscordDaemon.start_discord_daemon, (settings.discord_token,))
launch_daemon_thread(MessengerDaemon.start_messenger_daemon, (settings.messenger_email, settings.messenger_password,))

Scheduler.run()
