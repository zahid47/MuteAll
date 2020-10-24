import discord
from discord.ext import commands
import os

# For local testing only
# with open("TOKEN.txt") as file:
#     TOKEN = file.read()

TOKEN = os.environ["TOKEN"]

client = commands.Bot(command_prefix=".")


# sets status when the bot is ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(".mute | .unmute"))
    # print("Ready!")


# removes the default ".help" command
client.remove_command("help")


# shows help text
@client.command(aliases=["commands", "Help", "h", "H"])
async def help(ctx):
    embed = discord.Embed()
    embed.set_author(name="Available Commands")
    embed.add_field(name="`.ping`", value="Latency of the bot", inline=False)
    embed.add_field(name="`.mute` / `.m`", value="Mutes everyone in your current voice channel, both you and the bot "
                                                 "require `Mute Members` permission", inline=False)
    embed.add_field(name="`.unmute` / `.u`", value="Un-mutes everyone in your current voice channel, only the bot "
                                                   "requires `Mute Members` permission", inline=False)
    embed.add_field(name="`.xm`", value="Experimental mute (useful if you use a music bot). Mutes humans and un-mutes "
                                        "bots in your current voice channel. Both you and the bot require `Mute "
                                        "Members` permission", inline=False)
    embed.add_field(name="`.xu`",
                    value="Experimental un-mute (useful if you use a music bot). Un-mutes humans and mutes "
                          "bots in your current voice channel. Only the bot requires `Mute Members` permission",
                    inline=False)
    embed.add_field(name="_", value="[Join support server](https://discord.com/invite/Jxv66vm)", inline=False)

    await ctx.send(embed=embed)


# shows latency of the bot
@client.command(aliases=["latency"])
async def ping(ctx):
    await ctx.send(f"ping {round(client.latency * 1000)} ms")


# mutes everyone (except for bots) in the current voice channel
@client.command(aliases=["m", "M", "Mute"])
async def mute(ctx):
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            if ctx.author.guild_permissions.mute_members:  # check if the user has mute members permission
                try:  # try to mute if the bot has permissions
                    no_of_members = 0
                    for member in ctx.author.voice.channel.members:  # traverse through the members list in current vc
                        if not member.bot:  # check if member is a bot, don't mute if bot
                            await member.edit(mute=True)  # finally muting the member
                            no_of_members += 1
                    if no_of_members < 2:
                        await ctx.channel.send(f"Muted {no_of_members} user in {ctx.author.voice.channel}")
                    else:
                        await ctx.channel.send(f"Muted {no_of_members} users in {ctx.author.voice.channel}")
                except discord.errors.Forbidden:
                    await ctx.channel.send(  # the bot doesn't have the permission to mute
                        f"I don't have the `Mute Members` permission. Make sure I have the permission in my role "
                        f"**and** in your current voice channel `{ctx.author.voice.channel}`")
            else:
                await ctx.channel.send("You don't have the `Mute Members` permission")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}). Please contact my sensei`SCARECOW#0456`")


# [experimental mute] mutes everyone in the current voice channel and mutes the bots, useful for music bots!
@client.command(aliases=["Xm"])
async def xm(ctx):
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            if ctx.author.guild_permissions.mute_members:  # check if the user has mute members permission
                try:  # try to mute if the bot has permissions
                    no_of_members = 0
                    for member in ctx.author.voice.channel.members:  # traverse through the members list in current vc
                        if not member.bot:  # check if member is not a bot
                            await member.edit(mute=True)  # mute the non-bot member
                            no_of_members += 1
                        else:
                            await member.edit(mute=False)  # un-mute the bot member
                            await ctx.send(f"Un-muted {member.name}")
                    if no_of_members < 2:
                        await ctx.channel.send(f"Un-muted {no_of_members} user in {ctx.author.voice.channel}")
                    else:
                        await ctx.channel.send(f"Un-muted {no_of_members} users in {ctx.author.voice.channel}")
                except discord.errors.Forbidden:
                    await ctx.channel.send(  # the bot doesn't have the permission to mute
                        f"I don't have the `Mute Members` permission. Make sure I have the permission in my role "
                        f"**and** in your current voice channel `{ctx.author.voice.channel}`")
            else:
                await ctx.channel.send("You don't have the `Mute Members` permission")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}). Please contact my sensei`SCARECOW#0456`")


# un-mutes everyone (except for bots) in the current voice channel
@client.command(aliases=["um", "un", "un-mute", "u", "U", "Un", "Um", "Unmute"])
async def unmute(ctx):
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            try:  # try to un-mute if the bot has permissions
                no_of_members = 0
                for member in ctx.author.voice.channel.members:  # traverse through the members list in current vc
                    if not member.bot:  # check if member is a bot, don't un-mute if bot
                        await member.edit(mute=False)  # finally un-muting the member
                        no_of_members += 1
                if no_of_members < 2:
                    await ctx.channel.send(f"Un-muted {no_of_members} user in {ctx.author.voice.channel}")
                else:
                    await ctx.channel.send(f"Un-muted {no_of_members} users in {ctx.author.voice.channel}")
            except discord.errors.Forbidden:
                await ctx.channel.send(  # the bot doesn't have the permission to mute
                    f"I don't have the `Mute Members` permission. Make sure I have the permission in my role "
                    f"**and** in your current voice channel `{ctx.author.voice.channel}`")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}). Please contact my sensei`SCARECOW#0456`")


# [experimental un-mute] un-mutes everyone in the current voice channel and mutes the bots, useful for music bots!
@client.command(aliases=["Xu"])
async def xu(ctx):
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            try:  # try to un-mute if the bot has permissions
                no_of_members = 0
                for member in ctx.author.voice.channel.members:  # traverse through the members list in current vc
                    if not member.bot:  # check if member is not a bot
                        await member.edit(mute=False)  # un-mute the non-bot member
                        no_of_members += 1
                    else:
                        await member.edit(mute=True)  # mute the bot member
                        await ctx.send(f"Muted {member.name}")
                if no_of_members < 2:
                    await ctx.channel.send(f"Un-muted {no_of_members} user in {ctx.author.voice.channel}")
                else:
                    await ctx.channel.send(f"Un-muted {no_of_members} users in {ctx.author.voice.channel}")
            except discord.errors.Forbidden:
                await ctx.channel.send(  # the bot doesn't have the permission to mute
                    f"I don't have the `Mute Members` permission. Make sure I have the permission in my role "
                    f"**and** in your current voice channel `{ctx.author.voice.channel}`")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}). Please contact my sensei`SCARECOW#0456`")


# run the bot
client.run(TOKEN)
