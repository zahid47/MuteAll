import discord
from discord.ext import commands
import random
import time
import os

TOKEN = os.environ["TOKEN"]

client = commands.Bot(command_prefix=".")


# sets status when the bot is ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(".help"))
    print("Ready!")


# removes the default ".help" command
client.remove_command("help")


# shows help text
@client.command(aliases=["commands", "Help", "h", "H"])
@commands.cooldown(1, 3)
async def help(ctx):
    embed = discord.Embed()
    embed.set_author(name="Available Commands")

    embed.add_field(name="`.ping`", value="Latency of the bot", inline=False)

    embed.add_field(name="`.invite`", value="Invite link", inline=False)

    embed.add_field(name="`.mute` / `.m`", value="Mute humans and un-mute bots in your current voice channel, "
                                                 "both you and the bot require `Mute Members` permission",
                    inline=False)

    embed.add_field(name="`.unmute` / `.u`", value="Un-mute humans and mute bots in your current voice channel, "
                                                   "only the bot requires `Mute Members` permission",
                    inline=False)

    # embed.add_field(name="`.start` / `.s`", value="[BETA] React with emojies to mute or unmute, no need to type "
    #                                               "anymore! ", inline=False)

    embed.add_field(name="`.tanner` / `.t`", value="[BETA] Add a twist to the game! The bot randomly selects a user "
                                                   "in the voice channel to be the secret tanner. The tanner can only "
                                                   "win if people vote them off (and everyone else loses).",
                    inline=False)

    embed.add_field(name="_", value="[Join support server](https://discord.com/invite/Jxv66vm)", inline=False)

    await ctx.send(embed=embed)


# shows latency of the bot
@client.command(aliases=["latency"])
async def ping(ctx):
    await ctx.send(f"ping {round(client.latency * 1000)} ms")


# mutes everyone in the current voice channel and mutes the bots
@client.command(aliases=["m", "M", "Mute"])
async def mute(ctx):
    command_name = "mute"
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
                            # await ctx.send(f"Un-muted {member.name}")
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
        me = client.get_user(187568903084441600)
        await me.send(f"{command_name}: {e}")
        await ctx.channel.send(f"Something went wrong ({e}). `SCARECOW#0456` was notified.")


# un-mutes everyone in the current voice channel and mutes the bots
@client.command(aliases=["um", "un", "un-mute", "u", "U", "Un", "Um", "Unmute"])
@commands.cooldown(1, 3)
async def unmute(ctx):
    command_name = "unmute"
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
                        # await ctx.send(f"Muted {member.name}")
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
        me = client.get_user(187568903084441600)
        await me.send(f"{command_name}: {e}")
        await ctx.channel.send(f"Something went wrong ({e}). `SCARECOW#0456` was notified.")


# handling the unmute cooldown error if they spam it
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Wait 3 seconds before using this again!")


# temp
@client.command(aliases=["Xm"])
async def xm(ctx):
    await ctx.send("`.xm` is now `.m`. So just use that instead.")


# temp
@client.command(aliases=["Xu"])
async def xu(ctx):
    await ctx.send("`.xu` is now `.u`. So just use that instead.")


# tanner role
@client.command(aliases=["Tanner", "t", "T"])
@commands.cooldown(1, 60)
async def tanner(ctx):
    command_name = "tanner"
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            members_list = []
            for member in ctx.author.voice.channel.members:  # traverse through the members list in current vc
                if not member.bot:  # check if member is not a bot
                    members_list.append(member)
            selected_tanner = random.choice(members_list)
            await selected_tanner.send(f"[Initiated by {ctx.author.name}] You are the secret Tanner! If you were "
                                       f"already an Impostor then nothing changes. But if you were a crewmate, "
                                       f"now you are the Tanner! The only way to win is by making everyone else to "
                                       f"vote you off. Act sus!")
            await ctx.send("Selected a Tanner and sent them a DM!")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        me = client.get_user(187568903084441600)
        await me.send(f"{command_name}: {e}")
        await ctx.channel.send(f"Something went wrong ({e}). `SCARECOW#0456` was notified.")


# handling the tanner cooldown error if they spam it
@tanner.error
async def tanner_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Wait 60 seconds before using this again!")


@client.command(aliases=["i", "link"])
async def invite(ctx):
    await ctx.send("Invite Link: <https://discord.com/oauth2/authorize?client_id=757369495953342593&scope=bot"
                   "&permissions=4205632>")


# # use reactions instead of typing
# @client.command(aliases=["play", "s", "p"])
# async def start(ctx):
#     try:
#
#         server_id = ctx.guild.id
#         print(server_id)
#
#         await ctx.send("IMPORTANT! Make sure the bot has `Add Reactions` and `Manage Messages` permission!")
#         embed = discord.Embed()
#         embed.add_field(name="Started a new game! React with an emoji below.", value=":regional_indicator_m: is mute, "
#                                                                                      ":regional_indicator_u: is unmute",
#                         inline=False)
#         message = await ctx.send(embed=embed)
#         await message.add_reaction("🇲")
#         await message.add_reaction("🇺")
#
#         @client.event
#         async def on_reaction_add(reaction, user):
#             if user != client.user:
#                 if reaction.emoji == "🇲":
#                     await mute(ctx)
#                     await reaction.remove(user)
#                     time.sleep(2)
#                     await ctx.channel.purge(limit=1)
#                 elif reaction.emoji == "🇺":
#                     await unmute(ctx)
#                     await reaction.remove(user)
#                     time.sleep(2)
#                     await ctx.channel.purge(limit=1)
#                 else:
#                     await reaction.clear()
#
#     except Exception as e:
#         me = client.get_user(187568903084441600)
#         await me.send(e)
#         await ctx.channel.send(f"Something went wrong ({e}). `SCARECOW#0456` was notified.")

# run the bot
client.run(TOKEN)
