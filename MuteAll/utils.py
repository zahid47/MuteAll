import discord
from MuteAll.errors import show_common_error, show_permission_error


def get_help():
    embed = discord.Embed()

    embed.set_author(name="Help")

    embed.add_field(name="Slash Commands",
                    value="Press / to view all the available commands", inline=False)

    embed.add_field(name="Bot not muting everyone?",
                    value="Ask everyone to reconnect to the voice channel.", inline=False)

    embed.add_field(
        name="Need more help?", value="[Join support server](https://discord.gg/8hrhffR6aX)", inline=False)

    return embed


async def handle_errors(ctx, bot, function, mentions):
    try:
        await function(ctx, mentions)

    except discord.Forbidden:  # the bot doesn't have the permission to do this
        return await show_permission_error(ctx)
    except Exception as e:
        return await show_common_error(ctx, bot, e)


def can_do(ctx, requiredPermissions=[]):
    if not ctx.guild:
        return "This does not work in DMs"

    if not ctx.author.voice:
        return "You must join a voice channel first"

    if "mute" in requiredPermissions:
        if not ctx.author.guild_permissions.mute_members:
            return "You don't have the `Mute Members` permission"

    if "defean" in requiredPermissions:
        if not ctx.author.guild_permissions.deafen_members:
            return "You don't have the `Deafen Members` permission"

    return "OK"


def has_role(member, role_id):

    role_ids = []
    for role in member.roles:
        role_ids.append(role.id)

    if role_id in role_ids:
        return True
    return False


def get_affected_users(ctx, mentions):

    mentions: list = mentions.split(" ")
    affected_users = []

    for mention in mentions:

        # check if they actually mentioned a user or role
        if len(mention) != 22:
            continue

        if mention[2] == "&":  # 3rd element == & means they mentioned a role
            for member in ctx.author.voice.channel.members:
                role_id = int(mention[3:-1])
                if has_role(member, role_id):
                    affected_users.append(member)
        else:
            for member in ctx.author.voice.channel.members:
                if member.id == int(mention[3:-1]):
                    affected_users.append(member)

    return affected_users


def get_stats(bot):

    guilds = bot.guilds
    no_of_guilds = len(guilds)
    no_of_members = 0

    for guild in guilds:
        no_of_members = no_of_members + guild.member_count

    return no_of_guilds, no_of_members


# def remove_empty_items(arr: list):
#     non_empty_arr: list = []

#     for item in arr:
#         if len(item) > 1:
#             non_empty_arr.append(item)

#     return non_empty_arr


# async def help(ctx):
#     embed = discord.Embed(color=discord.Color.lighter_grey())

#     embed.set_author(name="Available Commands")

#     embed.add_field(name="`.ping`", value="latency of the bot", inline=False)

#     embed.add_field(name="`.changeprefix <your prefix here>`",
#                     value="change the prefix for your server (only admin can use this!)", inline=False)

#     embed.add_field(name="`.viewprefix`",
#                     value="view prefix for your server", inline=False)

#     embed.add_field(name="`.mute` / `.m`", value="Mute humans and un-mute bots in your current voice channel.",
#                     inline=False)

#     embed.add_field(name="`.unmute` / `.u`", value="Un-mute humans and mute bots in your current voice channel.",
#                     inline=False)

#     embed.add_field(name="`.deafen` / `.d`", value="Deafen everyone in your current voice channel.",
#                     inline=False)

#     embed.add_field(name="`.undeafen` / `.ud`", value="Un-deafen everyone in your current voice channel.",
#                     inline=False)

#     embed.add_field(name="`.undeafenme` / `.udme`", value="Un-deafen only yourself.",
#                     inline=False)

#     embed.add_field(name="`.all` / `.a`", value="Mute and Deafen everyone in your current voice channel.",
#                     inline=False)

#     embed.add_field(name="`.unall` / `.ua`", value="Un-mute and Un-deafen everyone in your current voice channel.",
#                     inline=False)

#     embed.add_field(name="`.end` / `.e`",
#                     value="End the game, un-mute and un-deafen everyone (including bots)", inline=False)

#     embed.add_field(name="Bot not muting everyone?",
#                     value="Ask everyone to reconnect to the voice channel.", inline=False)

#     embed.add_field(
#         name="_", value="[Join support server](https://discord.gg/8hrhffR6aX)", inline=False)

#     await ctx.send(embed=embed)
