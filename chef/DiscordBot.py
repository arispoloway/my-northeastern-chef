import discord
import asyncio
from chef.Configuration import Configuration

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
        await callbacks[message.channel.id].receive_new_message(message.content)


def listen_to_channel(channel_id : str, callback : Configuration):
    callbacks[channel_id] = callback

async def send_message(channel_id : str, message : str):
    channel = client.get_channel(channel_id)
    if channel == None:
        raise Exception("Invalid channel")
    await client.send_message(channel, message)


def start_discord_bot():
    client.run("token")