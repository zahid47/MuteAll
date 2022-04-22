import discord
from discord.ext import commands


async def help(ctx):
    embed = discord.Embed(color=discord.Color.lighter_grey())

    embed.set_author(name="Available Commands")

    embed.add_field(name="`.ping`", value="latency of the bot", inline=False)

    embed.add_field(name="`.changeprefix <your prefix here>`",
                    value="change the prefix for your server (only admin can use this!)", inline=False)

    embed.add_field(name="`.viewprefix`",
                    value="view prefix for your server", inline=False)

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

    embed.add_field(name="`.all` / `.a`", value="Mute and Deafen everyone in your current voice channel.",
                    inline=False)

    embed.add_field(name="`.unall` / `.ua`", value="Un-mute and Un-deafen everyone in your current voice channel.",
                    inline=False)

    embed.add_field(name="`.end` / `.e`",
                    value="End the game, un-mute and un-deafen everyone (including bots)", inline=False)

    embed.add_field(name="Bot not muting everyone?",
                    value="Ask everyone to reconnect to the voice channel.", inline=False)

    embed.add_field(
        name="_", value="[Join support server](https://discord.gg/8hrhffR6aX)", inline=False)

    await ctx.send(embed=embed)


def can_do(ctx):
    if not ctx.guild:
        return "This does not work in DMs"

    if not ctx.author.voice:
        return "You must join a voice channel first"

    if not ctx.author.guild_permissions.mute_members:
        return "You don't have the `Mute Members` permission"

    return "OK"


def has_role(member, role_id):

    role_ids = []
    for role in member.roles:
        role_ids.append(role.id)

    if role_id in role_ids:
        return True
    return False


async def get_affected_users(ctx, args):

    mentioned_users = []

    for user in args:

        # check if they actually mentioned a user or role
        if len(user) != 22 and len(user) != 21:
            return []

        if user[2] == "&":  # 3rd element == & means they mentioned a role
            for member in ctx.author.voice.channel.members:
                role_id = int(user[3:-1])
                if has_role(member, role_id):
                    mentioned_users.append(member)
        else:
            for member in ctx.author.voice.channel.members:
                if member.id == int(user[2:-1]):
                    mentioned_users.append(member)

    return mentioned_users


async def stats(ctx, client):

    guilds = client.guilds
    no_of_guilds = len(guilds)
    no_of_members = 0

    for guild in guilds:
        no_of_members = no_of_members + guild.member_count

    await ctx.send(f"MuteAll is serving a total of {no_of_members} users in {no_of_guilds} servers!")
