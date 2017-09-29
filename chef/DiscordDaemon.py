import asyncio

import discord


import chef.configuration.ConfigurationCreator

import chef.configuration.ConfigurationSettings
import chef.configuration.DiscordConfiguration

client = discord.Client()

callbacks = {}


@client.event
async def on_ready():
    print("Discord Daemon Connected")
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)


@client.event
async def on_message(message : discord.Message):
    if message.channel.id in callbacks:
        callbacks[message.channel.id].receive_new_message(message.content)
    else:
        if message.content.startswith("!register"):
            configuration_settings = chef.configuration.ConfigurationSettings.create_new_settings(chef.configuration.DiscordConfiguration.get_configuration_type(), message.channel.id)
            configuration_settings.set("discord-channel-id", message.channel.id)
            chef.configuration.ConfigurationCreator.create_configuration_from_settings(configuration_settings)


def subscribe_to_channel(channel_id : str, callback):
    callbacks[channel_id] = callback


def send_message(channel_id : str, message : str):
    channel = client.get_channel(channel_id)
    if not channel:
        raise Exception("Invalid channel")
    asyncio.run_coroutine_threadsafe(client.send_message(channel, message), client.loop)


def start_discord_daemon(token):
    client.run(token)