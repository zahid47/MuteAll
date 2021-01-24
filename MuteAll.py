import discord
from discord.ext import commands
import random
import os
import asyncio

# TOKEN = os.environ["TOKEN"]
TOKEN = "NzY5NTM1MzIzOTkzNTM4NjEw.X5Qbng.ZsoI1ZOFBJugswDZFE5CMyrdPm4"

client = commands.AutoShardedBot(command_prefix="?")

client.remove_command("help")  # removes the default ".help" command


# sets status when the bot is ready
@client.event
async def on_ready():
    activity = discord.Activity(name=".help", type=discord.ActivityType.playing)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Ready!")


# send a help msg when the bot joins a server
@client.event
async def on_guild_join(guild):
    embed = discord.Embed()
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed.add_field(name="Hey, thanks for adding me!", value="If you are already in a voice channel, please make "
                                 "everyone disconnect and reconnect so I can work properly. Type `.help` to view all "
                                 "the commands.")
            await channel.send(embed=embed)
            break


# invite link for the bot
@client.command(aliases=["i", "link"])
async def invite(ctx):
    embed = discord.Embed()
    embed.add_field(name="Invite Link", value="[Invite The Bot](https://discord.com/oauth2/authorize?client_id=757369495953342593&scope=bot&permissions=12659776)")

    await ctx.send(embed=embed)


# shows latency of the bot
@client.command(aliases=["latency"])
async def ping(ctx):
    embed = discord.Embed()
    embed.add_field(name="Ping", value=f"{round(client.latency * 1000)} ms")

    await ctx.send(embed=embed)


# shows help text
@client.command(aliases=["commands", "Help", "h", "H"])
async def help(ctx):
    embed = discord.Embed(color=discord.Color.lighter_grey())

    embed.set_author(name="Available Commands")

    embed.add_field(name="`.ping`", value="Latency of the bot", inline=False)

    embed.add_field(name="`.invite`", value="Invite link", inline=False)

    embed.add_field(name="`.mute` / `.m`", value="Mute humans and un-mute bots in your current voice channel.",
                    inline=False)

    embed.add_field(name="`.unmute` / `.u`", value="Un-mute humans and mute bots in your current voice channel.",
                    inline=False)

    embed.add_field(name="`.deafen` / `.d`", value="Deafen everyone in your current voice channel.",
                    inline=False)

    embed.add_field(name="`.undeafen` / `.ud`", value="Un-deafen everyone in your current voice channel.",
                    inline=False)

    embed.add_field(name="`.undeafenme` / `.udme`", value="Un-deafen only yourself.",
                    inline=False)

    embed.add_field(name="`.start` / `.s`", value="[BETA] React with emojies to mute or unmute, no need to type "
                                                  "anymore! ", inline=False)

    embed.add_field(name="`.end` / `.e`", value="End the game, un-mute everyone (including bots)", inline=False)

    embed.add_field(name="`.tanner` / `.t`", value="Add a new role to the game! The bot randomly selects a user "
                                                   "in the voice channel to be the secret tanner. The tanner can only "
                                                   "win if people vote them off (and everyone else loses).",
                    inline=False)
    embed.add_field(name="`.minion` / `.min`", value="Add a new role to the game! The bot randomly selects a user "
                                                     "in the voice channel to be the secret minion. The minion is like "
                                                     "another impostor but can not kill or sabotage, they will try to "
                                                     "keep the sus away from the impostors and they will if the "
                                                     "impostors win.",
                    inline=False)
    embed.add_field(name="Bot not muting everyone?", value="Make everyone disconnect and reconnect to the Voice "
                                                           "Channel again.", inline=False)

    embed.add_field(name="_", value="[Join support server](https://discord.gg/8hrhffR6aX)", inline=False)

    await ctx.send(embed=embed)


# mutes everyone in the current voice channel and un-mutes the bots
@client.command(aliases=["m", "M", "Mute"])
async def mute(ctx):
    # command_name = "mute"
    author = ctx.author  # command author
    embed = discord.Embed(color=discord.Color.red())
    botEmbed = discord.Embed(color=discord.Color.green())

    if ctx.guild:  # check if the msg was in a server's text channel
        if author.voice:  # check if the user is in a voice channel
            if author.guild_permissions.mute_members:  # check if the user has mute members permission
                try:
                    no_of_members = 0
                    for member in author.voice.channel.members:  # traverse through the members list in current vc
                        if not member.bot:  # check if member is not a bot
                            await member.edit(mute=True)  # mute the non-bot member
                            no_of_members += 1
                        else:
                            await member.edit(mute=False)  # un-mute the bot member
                            embed.clear_fields()
                            botEmbed.set_author(name=f"Un-muted {member.name}")
                            await ctx.send(embed=botEmbed)
                            # embed.add_field(name="Status", value=f"Un-muted {member.name}")
                    if no_of_members == 0:
                        embed.clear_fields()
                        embed.set_author(name="Everyone, please reconnect to the voice channel.")
                        # embed.add_field(name="Error", value="Everyone, please reconnect to the voice channel.")
                    else:
                        embed.clear_fields()
                        embed.set_author(name=f"Muted {no_of_members} user(s)")
                        # embed.add_field(name="Status", value=f"Muted {no_of_members} users.")
                    await ctx.send(embed=embed)

                except discord.Forbidden: # the bot doesn't have the permission to mute
                    embed.clear_fields()
                    embed.add_field(name="No Permission", value=f"""
                    Please make sure I have the `Mute Members` permission in my role **and** in your current voice channel `{author.voice.channel}`.
                    If it is still not working, try giving me the 'administrator' permission.
                    """)
                    await ctx.send(embed=embed)
                # except discord.HTTPException as e:
                #     # # me = client.get_user(187568903084441600)
                #     # await me.send(f"{command_name} caused HTTPException: {e}")
                #     embed.add_field(name="Something went wrong. You can try the following things:", value="""
                #     1. Make everyone disconnect and reconnect to the Voice Channel again.
                #     2. Give me the 'Administrator' permission.
                #     3. DM 'SCARECOW#0456' on discord.
                #     """)
                #     await ctx.send(embed=embed)
                except Exception as e:
                    # me = client.get_user(187568903084441600)
                    # await me.send(f"{command_name} caused other: {e}")
                    embed.clear_fields()
                    embed.add_field(name="Something went wrong. You can try the following things:", value="""
                    1. Make everyone disconnect and reconnect to the Voice Channel again.
                    2. Give me the 'Administrator' permission.
                    3. DM `SCARECOW#0456` on discord.
                    """)
                    await ctx.send(embed=embed)
            else:
                embed.clear_fields()
                embed.add_field(name="Error", value="You don't have the `Mute Members` permission.")
                await ctx.send(embed=embed)
        else:
            embed.clear_fields()
            embed.add_field(name="Error", value="You must join a voice channel first.")
            await ctx.send(embed=embed)
    else:
        embed.clear_fields()
        embed.add_field(name="Error", value="This does not work in DMs.")
        await ctx.send(embed=embed)


# deafens everyone in the current voice channel
@client.command(aliases=["d", "Deafen"])
async def deafen(ctx):
    command_name = "deafen"
    author = ctx.author

    if ctx.guild:  # check if the msg was in a server's text channel
        if author.voice:  # check if the user is in a voice channel
            if author.guild_permissions.deafen_members:  # check if the user has deafen members permission
                try:
                    no_of_members = 0
                    for member in author.voice.channel.members:  # traverse through the members list in current vc
                        await member.edit(deafen=True)  # deafen the member
                        no_of_members += 1
                    if no_of_members == 0:
                        await ctx.channel.send(f"Everyone, please disconnect and reconnect to the Voice Channel again.")
                    elif no_of_members < 2:
                        await ctx.channel.send(f"Deafened {no_of_members} user in {author.voice.channel}.")
                    else:
                        await ctx.channel.send(f"Deafened {no_of_members} users in {author.voice.channel}.")

                except discord.Forbidden:
                    await ctx.channel.send(  # the bot doesn't have the permission to mute
                        f"Please make sure I have the `Deafen Members` permission in my role **and** in your current "
                        f"voice channel `{author.voice.channel}`.")
                except discord.HTTPException as e:
                    # me = client.get_user(187568903084441600)
                    # await me.send(f"{command_name} caused HTTPException: {e}")
                    await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                           "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                           "2. Give me the 'Administrator' permission.\n"
                                           "3. DM `SCARECOW#0456` on discord.\n")
                except Exception as e:
                    # me = client.get_user(187568903084441600)
                    # await me.send(f"{command_name} caused other: {e}")
                    await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                           "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                           "2. Give me the 'Administrator' permission.\n"
                                           "3. DM `SCARECOW#0456` on discord.\n")
            else:
                await ctx.channel.send("You don't have the `Deafen Members` permission.")
        else:
            await ctx.send("You must join a voice channel first.")
    else:
        await ctx.send("This does not work in DMs.")


# un-mutes everyone in the current voice channel and mutes the bots
@client.command(aliases=["um", "un", "un-mute", "u", "U", "Un", "Um", "Unmute"])
async def unmute(ctx):
    command_name = "unmute"
    author = ctx.author  # command author
    embed = discord.Embed(color=discord.Color.green())
    botEmbed = discord.Embed(color=discord.Color.red())

    if ctx.guild:  # check if the msg was in a server's text channel
        if author.voice:  # check if the user is in a voice channel
            try:
                no_of_members = 0
                for member in author.voice.channel.members:  # traverse through the members list in current vc
                    if not member.bot:  # check if member is not a bot
                        await member.edit(mute=False)  # unmute the non-bot member
                        no_of_members += 1
                    else:
                        await member.edit(mute=True)  # mute the bot member
                        embed.clear_fields()
                        botEmbed.set_author(name=f"Muted {member.name}")
                        await ctx.send(embed=botEmbed)
                        # embed.add_field(name="Status", value=f"Un-muted {member.name}")
                if no_of_members == 0:
                    embed.clear_fields()
                    embed.set_author(name="Everyone, please reconnect to the voice channel.")
                    # embed.add_field(name="Error", value="Everyone, please reconnect to the voice channel.")
                else:
                    embed.clear_fields()
                    embed.set_author(name=f"Un-muted {no_of_members} user(s)")
                    # embed.add_field(name="Status", value=f"Muted {no_of_members} users.")
                await ctx.send(embed=embed)

            except discord.Forbidden: # the bot doesn't have the permission to mute
                embed.clear_fields()
                embed.add_field(name="No Permission", value=f"""
                Please make sure I have the `Mute Members` permission in my role **and** in your current voice channel `{author.voice.channel}`.
                If it is still not working, try giving me the 'administrator' permission.
                """)
                await ctx.send(embed=embed)
            # except discord.HTTPException as e:
            #     # # me = client.get_user(187568903084441600)
            #     # await me.send(f"{command_name} caused HTTPException: {e}")
            #     embed.add_field(name="Something went wrong. You can try the following things:", value="""
            #     1. Make everyone disconnect and reconnect to the Voice Channel again.
            #     2. Give me the 'Administrator' permission.
            #     3. DM 'SCARECOW#0456' on discord.
            #     """)
            #     await ctx.send(embed=embed)
            except Exception as e:
                # me = client.get_user(187568903084441600)
                # await me.send(f"{command_name} caused other: {e}")
                embed.clear_fields()
                embed.add_field(name="Something went wrong. You can try the following things:", value="""
                1. Make everyone disconnect and reconnect to the Voice Channel again.
                2. Give me the 'Administrator' permission.
                3. DM `SCARECOW#0456` on discord.
                """)
                await ctx.send(embed=embed)
        else:
            embed.clear_fields()
            embed.add_field(name="Error", value="You must join a voice channel first.")
            await ctx.send(embed=embed)
    else:
        embed.clear_fields()
        embed.add_field(name="Error", value="This does not work in DMs.")
        await ctx.send(embed=embed)
    

# un-deafens the user in the current voice channel
@client.command(aliases=["udme", "Undeafenme"])
async def undeafenme(ctx):
    command_name = "undeafenme"
    author = ctx.author

    if author.voice:  # check if the user is in a voice channel
        try:
            await author.edit(deafen=False)
            await ctx.send(f"Un-deafened {author.name}.")

        except discord.Forbidden:
            await ctx.channel.send(  # the bot doesn't have the permission to mute
                f"Please make sure I have the `Deafen Members` permission in my role **and** in your current "
                f"voice channel `{author.voice.channel}`.")
        except discord.HTTPException as e:
            # me = client.get_user(187568903084441600)
            # await me.send(f"{command_name} caused HTTPException: {e}")
            await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                   "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                   "2. Give me the 'Administrator' permission.\n"
                                   "3. DM `SCARECOW#0456` on discord.\n")
        except Exception as e:
            # me = client.get_user(187568903084441600)
            # await me.send(f"{command_name} caused other: {e}")
            await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                   "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                   "2. Give me the 'Administrator' permission.\n"
                                   "3. DM `SCARECOW#0456` on discord.\n")
    else:
        await ctx.send("You must join a voice channel first.")


# un-deafens everyone in the current voice channel
@client.command(aliases=["ud", "Undeafen"])
async def undeafen(ctx):
    command_name = "undeafen"
    author = ctx.author

    if ctx.guild:  # check if the msg was in a server's text channel
        if author.voice:  # check if the user is in a voice channel
            if author.guild_permissions.deafen_members:  # check if the user has deafen members permission
                try:
                    no_of_members = 0
                    for member in author.voice.channel.members:  # traverse through the members list in current vc
                        await member.edit(deafen=False)  # un-deafen the member
                        no_of_members += 1
                    if no_of_members == 0:
                        await ctx.channel.send(f"Everyone, please disconnect and reconnect to the Voice Channel again.")
                    elif no_of_members < 2:
                        await ctx.channel.send(f"Un-deafened {no_of_members} user in {author.voice.channel}.")
                    else:
                        await ctx.channel.send(f"Un-deafened {no_of_members} users in {author.voice.channel}.")

                except discord.Forbidden:
                    await ctx.channel.send(  # the bot doesn't have the permission to mute
                        f"Please make sure I have the `Deafen Members` permission in my role **and** in your current "
                        f"voice channel `{author.voice.channel}`.")
                except discord.HTTPException as e:
                    # me = client.get_user(187568903084441600)
                    # await me.send(f"{command_name} caused HTTPException: {e}")
                    await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                           "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                           "2. Give me the 'Administrator' permission.\n"
                                           "3. DM `SCARECOW#0456` on discord.\n")
                except Exception as e:
                    # me = client.get_user(187568903084441600)
                    # await me.send(f"{command_name} caused other: {e}")
                    await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                           "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                           "2. Give me the 'Administrator' permission.\n"
                                           "3. DM `SCARECOW#0456` on discord.\n")
            else:
                await ctx.channel.send("You don't have the `Mute Members` permission.")
        else:
            await ctx.send("You must join a voice channel first.")
    else:
        await ctx.send("This does not work in DMs.")


# end the game and un-mute everyone including bots
@client.command(aliases=["e", "E", "End"])
async def end(ctx):
    command_name = "end"
    author = ctx.author

    if ctx.guild:  # check if the msg was in a server's text channel
        if author.voice:  # check if the user is in a voice channel
            try:
                no_of_members = 0
                for member in author.voice.channel.members:  # traverse through the members list in current vc
                    await member.edit(mute=False)  # un-mute the member
                    no_of_members += 1
                if no_of_members == 0:
                    await ctx.channel.send(f"Everyone, please disconnect and reconnect to the Voice Channel again.")
                elif no_of_members < 2:
                    await ctx.channel.send(f"Un-muted {no_of_members} user in {author.voice.channel}.")
                else:
                    await ctx.channel.send(f"Un-muted {no_of_members} users in {author.voice.channel}.")

            except discord.Forbidden:
                await ctx.channel.send(  # the bot doesn't have the permission to mute
                    f"Please make sure I have the `Mute Members` permission in my role **and** in your current "
                    f"voice channel `{author.voice.channel}`.")
            except discord.HTTPException as e:
                # me = client.get_user(187568903084441600)
                # await me.send(f"{command_name} caused HTTPException: {e}")
                await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                       "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                       "2. Give me the 'Administrator' permission.\n"
                                       "3. DM `SCARECOW#0456` on discord.\n")
            except Exception as e:
                # me = client.get_user(187568903084441600)
                # await me.send(f"{command_name} caused other: {e}")
                await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                       "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                       "2. Give me the 'Administrator' permission.\n"
                                       "3. DM `SCARECOW#0456` on discord.\n")
        else:
            await ctx.send("You must join a voice channel first.")
    else:
        await ctx.send("This does not work in DMs.")


# tanner role
@client.command(aliases=["Tanner", "t", "T"])
async def tanner(ctx):
    command_name = "tanner"
    author = ctx.author

    DMEmbed = discord.Embed(color=discord.Color.gold())
    ReplayEmbed = discord.Embed(color=discord.Color.gold())

    if author.voice:  # check if the user is in a voice channel
        try:
            members_list = []
            for member in author.voice.channel.members:  # traverse through the members list in current vc
                if not member.bot:  # check if member is not a bot
                    members_list.append(member)
            selected_tanner = random.choice(members_list)

            DMEmbed.set_author(name="You are the secret Tanner!")
            DMEmbed.add_field(name="1.", value="If you were already an Impostor then nothing changes. But if you were "
                                               "a crewmate, now you are the Tanner!", inline=False)
            DMEmbed.add_field(name="2.", value="The only way to win is by making everyone else to vote you off. Act "
                                               "sus!", inline=False)

            await selected_tanner.send(embed=DMEmbed)

            ReplayEmbed.add_field(name="Selected a TANNER and sent them a DM.", value=f"Hey crewmates, there is a "
                                                                                      f"tanner among us! Find out who "
                                                                                      f"it is and vote 'em off! "
                                                                                      f" (Initiated by {author.name})",
                                  inline=False)
            await ctx.send(embed=ReplayEmbed)

        except IndexError:
            ReplayEmbed.add_field(name="Error", value="Everyone, please disconnect and reconnect to the Voice Channel "
                                                      "again.")
            await ctx.send(embed=ReplayEmbed)
        except Exception as e:
            # me = client.get_user(187568903084441600)
            # await me.send(f"{command_name}: {e}")
            await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                   "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                   "2. Give me the 'Administrator' permission.\n"
                                   "3. DM `SCARECOW#0456` on discord.\n")
    else:
        ReplayEmbed.add_field(name="Error", value="You must join a voice channel first")
        await ctx.send(embed=ReplayEmbed)


# minion role
@client.command(aliases=["Minion", "Min", "min"])
async def minion(ctx):
    command_name = "minion"
    author = ctx.author

    DMEmbed = discord.Embed(color=discord.Color.orange())  # the msg that we are gonna send to the dm of the selected minion
    ReplayEmbed = discord.Embed(color=discord.Color.orange())  # the msg that we are gonna send to the the server text channel

    if author.voice:  # check if the user is in a voice channel
        try:
            members_list = []
            for member in author.voice.channel.members:  # traverse through the members list in current vc
                if not member.bot:  # check if member is not a bot
                    members_list.append(member)
            selected_tanner = random.choice(members_list)

            DMEmbed.set_author(name="You are the secret Minion!")
            DMEmbed.add_field(name="1.", value="If you were already an Impostor then nothing changes. But if you were "
                                               "a crewmate, now you are the Minion of the Impostor!", inline=False)
            DMEmbed.add_field(name="2.", value="You are like the impostor but cannot kill or sabotage. You will win "
                                               "if the impostors win. Try to keep them alive!", inline=False)
            DMEmbed.add_field(name="3.", value="You and the impostor don't know each others identity.", inline=False)

            await selected_tanner.send(embed=DMEmbed)

            ReplayEmbed.add_field(name="Selected a MINION and sent them a DM.", value=f"Hey impostors, there is a "
                                                                                      f"minion among us! Try not to "
                                                                                      f"kill them, they will help you "
                                                                                      f"win!"
                                                                                      f" (Initiated by {author.name})",
                                  inline=False)
            await ctx.send(embed=ReplayEmbed)

        except IndexError:
            ReplayEmbed.add_field(name="Error", value="Everyone, please disconnect and reconnect to the Voice Channel "
                                                      "again.")
            await ctx.send(embed=ReplayEmbed)
        except Exception as e:
            # me = client.get_user(187568903084441600)
            # await me.send(f"{command_name}: {e}")
            await ctx.channel.send("Something went wrong. You can try the following things:\n"
                                   "1. Make everyone disconnect and reconnect to the Voice Channel again.\n"
                                   "2. Give me the 'Administrator' permission.\n"
                                   "3. DM `SCARECOW#0456` on discord.\n")
    else:
        ReplayEmbed.add_field(name="Error", value="You must join a voice channel first")
        await ctx.send(embed=ReplayEmbed)


async def mute_with_reaction(user):
    command_name = "mute_with_reaction"
    try:
        if user.voice:  # check if the user is in a voice channel
            if user.guild_permissions.mute_members:  # check if the user has mute members permission
                for member in user.voice.channel.members:  # traverse through the members list in current vc
                    if not member.bot:  # check if member is not a bot
                        await member.edit(mute=True)  # mute the non-bot member
                    else:
                        await member.edit(mute=False)  # un-mute the bot member
    except Exception as e:
        pass
        # me = client.get_user(187568903084441600)
        # await me.send(f"{command_name}: {e}")


async def unmute_with_reaction(user):
    command_name = "unmute_with_reaction"
    try:
        if user.voice:  # check if the user is in a voice channel
            for member in user.voice.channel.members:  # traverse through the members list in current vc
                if not member.bot:  # check if member is not a bot
                    await member.edit(mute=False)  # mute the non-bot member
                else:
                    await member.edit(mute=True)  # un-mute the bot member
    except Exception as e:
        pass
        # me = client.get_user(187568903084441600)
        # await me.send(f"{command_name}: {e}")


# async def end_with_reaction(user):
#     command_name = "end_with_reaction"
#     try:
#         if user.voice:  # check if the user is in a voice channel
#             for member in user.voice.channel.members:  # traverse through the members list in current vc
#                 await member.edit(mute=False)  # mute the non-bot member
#     except Exception as e:
#         # me = client.get_user(187568903084441600)
#         # await me.send(f"{command_name}: {e}")


# TODO: Move to on_raw_reaction_add(), get user obj using user_id, find a way to get reaction obj
# use reactions instead of typing
@client.command(aliases=["play", "s", "p"])
async def start(ctx):
    try:
        embed = discord.Embed()
        embed.add_field(name="React with an emoji below!", value=":regional_indicator_m: is mute, "
                                                                 ":regional_indicator_u: is unmute", inline=False)
        message = await ctx.send(embed=embed)

        await message.add_reaction("🇲")
        await message.add_reaction("🇺")

        # await message.add_reaction("🇪")

        @client.event
        async def on_reaction_add(reaction, user):
            try:
                if user != client.user:  # this user is the user who reacted, ignore the initial reactions from the bot
                    if reaction.message.author == client.user:  # this user is the author of the embed, should be the
                        # bot itself, this check is needed so the bot doesn't mute/unmute on reactions to any other
                        # messages
                        if reaction.emoji == "🇲":
                            await mute_with_reaction(user)
                            await reaction.remove(user)

                        elif reaction.emoji == "🇺":
                            await unmute_with_reaction(user)
                            await reaction.remove(user)

                        # elif reaction.emoji == "🇪":
                        #     await end_with_reaction(user)
                        #     await reaction.remove(user)

            except discord.errors.Forbidden:
                await ctx.send("Make sure I have the following permissions: `Manage Messages`, `Read Message History`, "
                               "`Add Reactions`, `Mute Members`")

    except discord.errors.Forbidden:
        await ctx.send("Make sure I have the following permissions: `Manage Messages`, `Read Message History`, "
                       "`Add Reactions`, `Mute Members`")

    except discord.errors.NotFound:
        await ctx.channel.send(f"Something went wrong. Try rejoining the VC. Also make sure the bot has the following "
                               f"permissions: `Manage Messages`, `Read Message History`, `Add Reactions`, "
                               f"`Mute Members`, `Deafen Members`. Please contact `SCARECOW#0456` if this keeps "
                               f"happening. OR use the normal `.mute` and `.unmute`")

    except discord.errors.HTTPException:
        await ctx.channel.send(f"Something went wrong. Try rejoining the VC. Also make sure the bot has the following "
                               f"permissions: `Manage Messages`, `Read Message History`, `Add Reactions`, "
                               f"`Mute Members`, `Deafen Members`. Please contact `SCARECOW#0456` if this keeps "
                               f"happening. OR use the normal `.mute` and `.unmute`")

    except Exception as e:
        # me = client.get_user(187568903084441600)
        # await me.send(e)
        await ctx.channel.send(f"Something went wrong. Try rejoining the VC. Also make sure the bot has the following "
                               f"permissions: `Manage Messages`, `Read Message History`, `Add Reactions`, "
                               f"`Mute Members`, `Deafen Members`. Please contact `SCARECOW#0456` if this keeps "
                               f"happening. OR use the normal `.mute` and `.unmute`")


# hotkey
# @client.command()
# async def a(ctx):
#     while True:
#         if ctx.author.voice.self_mute:
#             await mute(ctx)
#         await asyncio.sleep(1)

# run the bot
client.run(TOKEN)
