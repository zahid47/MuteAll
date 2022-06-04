import discord
import os
from MuteAll import events, utils, core

bot = discord.AutoShardedBot()


# sets status when the bot is ready
@bot.event
async def on_ready():
    await events.on_ready(bot)


@bot.slash_command(name="ping", description="show latency of the bot")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! {round(bot.latency * 1000)} ms")


@bot.slash_command(name="help", description="get some help!")
async def help(ctx: discord.ApplicationContext):
    await utils.help(ctx)


@bot.slash_command(name="mute", description="server mute people!")
async def mute(ctx: discord.ApplicationContext,
               mentions: discord.Option(str, "mention user(s) or role(s)") = ""):

    can_do = utils.can_do(ctx)
    if can_do != "OK":
        return await ctx.respond(can_do)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = utils.get_affected_users(ctx, mentions)

    await core.do(ctx, task="mute", members=members)
    await ctx.respond("👍")


@bot.slash_command(name="unmute", description="unmute people!")
async def unmute(ctx: discord.ApplicationContext,
                 mentions: discord.Option(str, "mention user(s) or role(s)") = ""):

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = utils.get_affected_users(ctx, mentions)

    await core.do(ctx, task="unmute", members=members)
    await ctx.respond("👍")


@bot.slash_command(name="deafen", description="deafen people!")
async def deafen(ctx: discord.ApplicationContext,
                 mentions: discord.Option(str, "mention user(s) or role(s)") = ""):
    can_do = utils.can_do(ctx)
    if can_do != "OK":
        return await ctx.respond(can_do)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = utils.get_affected_users(ctx, mentions)

    await core.do(ctx, task="deafen", members=members)
    await ctx.respond("👍")


@bot.slash_command(name="undeafen", description="undeafen people!")
async def undeafen(ctx: discord.ApplicationContext,
                   mentions: discord.Option(str, "mention user(s) or role(s)") = ""):

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = utils.get_affected_users(ctx, mentions)

    await core.do(ctx, task="undeafen", members=members)
    await ctx.respond("👍")


@bot.slash_command(name="all", description="mute and deafen people!")
async def all(ctx: discord.ApplicationContext,
              mentions: discord.Option(str, "mention user(s) or role(s)") = ""):

    can_do = utils.can_do(ctx)
    if can_do != "OK":
        return await ctx.respond(can_do)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = utils.get_affected_users(ctx, mentions)

    await core.do(ctx, task="all", members=members)
    await ctx.respond("👍")


@bot.slash_command(name="unall", description="unmute and undeafen people!")
async def unall(ctx: discord.ApplicationContext,
                mentions: discord.Option(str, "mention user(s) or role(s)") = ""):

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = utils.get_affected_users(ctx, mentions)

    await core.do(ctx, task="unall", members=members)
    await ctx.respond("👍")


@bot.slash_command(name="stats", description="show stats")
async def stats(ctx: discord.ApplicationContext):
    await utils.stats(ctx, bot)


# DEPRECATED
# # respond a help msg when the bot joins a server
# @bot.event
# async def on_guild_join(guild):
#     await events.on_guild_join(guild)


# @bot.command()
# async def changeprefix(ctx, prefix):
#     await prefixes.changeprefix(ctx, prefix)


# @bot.command(aliases=["prefix"])
# async def viewprefix(ctx):
#     await prefixes.viewprefix(ctx)

# @bot.command(aliases=["e", "E", "End"])
# async def end(ctx, *args):

#     if len(args) == 0:
#         members = ctx.author.voice.channel.members
#     else:
#         members = await utils.get_affected_users(ctx, args)

#     await core.do(ctx, task="end", members=members)

# @bot.command(aliases=["udme", "Undeafenme"])
# async def undeafenme(ctx):
#     await core.do(ctx, task="undeafen", members=[ctx.author])
# DEPRECATED

# run the bot
def run():
    bot.run(os.getenv("DISCORD_TOKEN"))
