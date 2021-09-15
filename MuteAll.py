import discord
from discord.ext import commands
import os
import json


TOKEN = os.environ["TOKEN"]

client = commands.AutoShardedBot(command_prefix="?")

@client.event
async def on_ready():
    activity = discord.Activity(
        name="maintenance", type=discord.ActivityType.playing)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Ready!")


@client.command()
async def dump(ctx):
    with open ("prefixes.json", "r") as f:
        data = json.load(f)
        print(data)

# run the bot
client.run(TOKEN)
