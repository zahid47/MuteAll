from discord.ext import commands
import os
from MuteAll import events, prefixes, utils, core, errors


# Discord Setup  ######################
client = commands.AutoShardedBot(command_prefix=prefixes.get_prefix)
client.remove_command("help")  # removes the default ".help" command
########################################


# sets status when the bot is ready
@client.event
async def on_ready():
    await events.on_ready(client)


# send a help msg when the bot joins a server
@client.event
async def on_guild_join(guild):
    await events.on_guild_join(guild)


@client.command()
async def changeprefix(ctx, prefix):
    await prefixes.changeprefix(ctx, prefix)


@client.command(aliases=["prefix"])
async def viewprefix(ctx):
    await prefixes.viewprefix(ctx)


@client.command(aliases=["latency"])
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)} ms")


@client.command(aliases=["commands", "Help", "h", "H"])
async def help(ctx):
    await utils.help(ctx)


@client.command(aliases=["m", "M", "Mute"])
async def mute(ctx, *args):

    can_do = utils.can_do(ctx)
    if can_do != "OK":
        return await ctx.send(can_do)

    if len(args) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = await utils.get_affected_users(ctx, args)

    await core.do(ctx, task="mute", members=members)


@client.command(aliases=["um", "un", "un-mute", "u", "U", "Un", "Um", "Unmute"])
async def unmute(ctx, *args):

    if len(args) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = await utils.get_affected_users(ctx, args)

    await core.do(ctx, task="unmute", members=members)


@client.command(aliases=["e", "E", "End"])
async def end(ctx, *args):

    if len(args) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = await utils.get_affected_users(ctx, args)

    await core.do(ctx, task="end", members=members)


@client.command(aliases=["d", "Deafen", "D"])
async def deafen(ctx, *args):
    can_do = utils.can_do(ctx)
    if can_do != "OK":
        return await ctx.send(can_do)

    if len(args) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = await utils.get_affected_users(ctx, args)

    await core.do(ctx, task="deafen", members=members)


@client.command(aliases=["udme", "Undeafenme"])
async def undeafenme(ctx):
    await core.do(ctx, task="undeafen", members=[ctx.author])


@client.command(aliases=["ud", "Undeafen"])
async def undeafen(ctx, *args):

    if len(args) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = await utils.get_affected_users(ctx, args)

    await core.do(ctx, task="undeafen", members=members)


@client.command(aliases=["a", "A"])
async def all(ctx, *args):
    can_do = utils.can_do(ctx)
    if can_do != "OK":
        return await ctx.send(can_do)

    if len(args) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = await utils.get_affected_users(ctx, args)

    await core.do(ctx, task="all", members=members)


@client.command(aliases=["ua", "Ua"])
async def unall(ctx, *args):

    if len(args) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = await utils.get_affected_users(ctx, args)

    await core.do(ctx, task="unall", members=members)


@client.command()
async def stats(ctx):
    await utils.stats(ctx, client)


# run the bot
def run():
    client.run(os.getenv("DISCORD_TOKEN"))
