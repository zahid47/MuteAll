import discord
from MuteAll.core import do_mute, do_unmute, do_deafen, do_undeafen, do_all, do_unall
from MuteAll.emojis import get_emojis
from MuteAll.errors import show_common_error


async def handle_ready(bot):
    activity = discord.Activity(
        name="for slash commands", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Logged in as {bot.user}")


async def handle_reaction(reaction, user, bot, ctx):
    # ignore initial reactions from the bot / self
    if user == bot.user:
        return

    # ignore reaction if message is not by the bot (basically don't mute if someone react to some other message)
    if reaction.message.author != bot.user:
        return

    # all checks passed, now do the thing!

    emojis = get_emojis(bot)

    if reaction.emoji == emojis["MUTE"]:
        await do_mute(ctx, [])
    elif reaction.emoji == emojis["UNMUTE"]:
        await do_unmute(ctx, [])
    elif reaction.emoji == emojis["DEAFEN"]:
        await do_deafen(ctx, [])
    elif reaction.emoji == emojis["UNDEAFEN"]:
        await do_undeafen(ctx, [])
    elif reaction.emoji == emojis["ALL"]:
        await do_all(ctx, [])
    elif reaction.emoji == emojis["UNALL"]:
        await do_unall(ctx, [])
    else:
        await show_common_error(ctx, "Reaction Error")

    await reaction.remove(user)


# DEPRECATED
# async def on_guild_join(guild):
#     embed = discord.Embed()
#     for channel in guild.text_channels:
#         if channel.permissions_for(guild.me).send_messages:
#             embed.add_field(name="Hey, thanks for adding me!",
#                             value="If you are already in a voice channel, please reconnect everyone. Type `.help` to view all the commands.")
#             await channel.send(embed=embed)
#             break
