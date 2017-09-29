import asyncio

import fbchat

from chef.configuration.ConfigurationCreator import ConfigurationCreator
from chef.configuration.ConfigurationSettings import ConfigurationSettings
from chef.configuration.MessengerConfiguration import MessengerConfiguration

client = fbchat.Client


callbacks = {}


@client.event
async def on_ready():
    print("Messenger Daemon Connected")
    print('Email: ' + client.email)
    print('Password: ' + client.password)


@client.event
async def on_message(message : ):

    if message.channel.id in callbacks:
        callbacks[message.channel.id].receive_new_message(message.content)
    else:
        if message.content.startswith("!register"):
            configuration_settings = ConfigurationSettings.create_new_settings(DiscordConfiguration.get_configuration_type(), message.channel.id)
            configuration_settings.set("discord-channel-id", message.channel.id)
            ConfigurationCreator.create_configuration_from_settings(configuration_settings)


def subscribe_to_channel(channel_id : str, callback : MessengerConfiguration):
    callbacks[channel_id] = callback


def send_message(channel_id : str, message : str):
    channel = client.get_channel(channel_id)
    if not channel:
        raise Exception("Invalid channel")
    asyncio.run_coroutine_threadsafe(client.send_message(channel, message), client.loop)


def start_messenger_daemon(email : str, password : str):
    client = fbchat.Client(email, password);

