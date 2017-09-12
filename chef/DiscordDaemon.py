import discord
import asyncio
import os
import shelve
from chef.Configuration import Configuration, DiscordConfiguration, ConfigurationCreator
from chef.ConfigurationSettings import ConfigurationSettings

client = discord.Client()

callbacks = {}

@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)

@client.event
async def on_message(message : discord.Message):
    if message.channel.id in callbacks:
        callbacks[message.channel.id].receive_new_message(message.content)
    else:
        if message.content.startswith("!register"):
            settings = ConfigurationSettings.create_new_settings(DiscordConfiguration.configuration_type, message.channel.id)
            settings.set("discord-channel-id", message.channel.id)
            new_configuration = ConfigurationCreator.create_configuration_from_settings(settings)


def subscribe_to_channel(channel_id : str, callback : DiscordConfiguration):
    callbacks[channel_id] = callback

async def send_message(channel_id : str, message : str):
    channel = client.get_channel(channel_id)
    if channel == None:
        raise Exception("Invalid channel")
    await client.send_message(channel, message)


def start_discord_daemon():
    client.run("token")