import discord
from discord.ext import commands
import os


# with open("TOKEN.txt") as file:
#     TOKEN = file.read()


TOKEN = os.environ["TOKEN"]

client = commands.Bot(command_prefix=".")


# send a msg when the bot is ready and set status
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(".mute | .unmute"))
    # print("Ready!")


# removes the default ".help" command
client.remove_command("help")


# show help text
@client.command(aliases=["commands", "Help", "h", "H"])
async def help(ctx):
    embed = discord.Embed()
    embed.set_author(name="Available Commands")
    embed.add_field(name="`.ping`", value="Latency of the bot", inline=False)
    embed.add_field(name="`.mute` / `.m`", value="Mutes everyone in your current voice channel, both you and the bot "
                                                 "require `Mute Members` permission", inline=False)
    embed.add_field(name="`.unmute` / `.u`", value="Unmutes everyone in your current voice channel, only the bot "
                                                   "requires `Mute Members` permission", inline=False)

    await ctx.send(embed=embed)


# get ping of the bot
@client.command(aliases=["latency"])
async def ping(ctx):
    await ctx.send(f"ping {round(client.latency * 1000)} ms")


# muting everyone in the current voice channel
# TODO only mute someone if they are not already muted
@client.command(aliases=["m", "stfu", "M", "Mute"])
async def mute(ctx):
    try:
        if ctx.author.voice:  # its true if the user is connected to a voice channel
            try:
                if ctx.author.guild_permissions.mute_members:  # its true if the user has mute_members permission
                    no_of_members = 0
                    # muted_members = []
                    for member in ctx.author.voice.channel.members:
                        await member.edit(mute=True)
                        no_of_members += 1
                        # muted_members.append(member.name)
                    await ctx.channel.send(f"Muted {no_of_members} user(s) in {ctx.author.voice.channel}.")
                else:
                    await ctx.channel.send("You don't have the `Mute Members` permission.")
            except discord.errors.Forbidden:
                await ctx.channel.send(f"I don't have the `Mute Members` permission. Please grant me the permission "
                                       f"in my role **and** in your "
                                       f"current voice channel `{ctx.author.voice.channel}`")
        else:
            await ctx.channel.send("You must be in a voice channel first.")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}) I'm still in testing phase. Please contact my sensei "
                               "<@!187568903084441600>")


# un-muting everyone in the current voice channel
@client.command(aliases=["um", "un", "un-mute", "u", "U", "Un", "Um", "Unmute"])
async def unmute(ctx):
    try:
        if ctx.author.voice:  # this will be true if the user is connected to a voice channel
            try:
                no_of_members = 0
                # muted_members = []
                for member in ctx.author.voice.channel.members:
                    await member.edit(mute=False)
                    no_of_members += 1
                    # muted_members.append(member.name)
                await ctx.channel.send(f"Un-muted {no_of_members} user(s) in {ctx.author.voice.channel}.")
            except discord.errors.Forbidden:
                await ctx.channel.send(f"I don't have the `Mute Members` permission. Please grant me the permission "
                                       f"in my role **and** in your "
                                       f"current voice channel `{ctx.author.voice.channel}`")
        else:
            await ctx.channel.send("You must be in a voice channel first.")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}) I'm still in testing phase. Please contact my sensei "
                               "<@!187568903084441600>")


# run the bot
client.run(TOKEN)
