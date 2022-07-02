import discord
from MuteAll.errors import show_common_error, show_permission_error
from MuteAll.utils import can_do, get_affected_users


async def do(ctx, task="mute", members=None):
    if members is None:
        members = []
    try:
        for member in members:
            match task:
                case "mute":
                    await member.edit(mute=True)
                case "unmute":
                    await member.edit(mute=False)
                case "end":
                    await member.edit(mute=False)
                case "deafen":
                    await member.edit(deafen=True)
                case "undeafen":
                    await member.edit(deafen=False)
                case "all":
                    await member.edit(mute=True)
                    await member.edit(deafen=True)
                case "unall":
                    await member.edit(mute=False)
                    await member.edit(deafen=False)

    except discord.Forbidden:  # the bot doesn't have the permission to mute
        return await show_permission_error(ctx)
    except Exception as e:
        return await show_common_error(ctx, e)


async def do_mute(ctx, mentions):
    canDo = can_do(ctx)
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(ctx, task="mute", members=members)


async def do_unmute(ctx, mentions):
    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(ctx, task="unmute", members=members)


async def do_deafen(ctx, mentions):
    canDo = can_do(ctx)
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(ctx, task="deafen", members=members)


async def do_undeafen(ctx, mentions):

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(ctx, task="undeafen", members=members)


async def do_all(ctx, mentions):

    canDo = can_do(ctx)
    if canDo != "OK":
        return await ctx.respond(canDo)

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(ctx, task="all", members=members)


async def do_unall(ctx, mentions):

    if len(mentions) == 0:
        members = ctx.author.voice.channel.members
    else:
        members = get_affected_users(ctx, mentions)

    await do(ctx, task="unall", members=members)


async def add_reactions(ctx, emojis):

    canDo = can_do(ctx)
    if canDo != "OK":
        return await ctx.respond(canDo)

    embed = discord.Embed()
    embed.set_author(name="Reaction Commands")  
    embed.add_field(name=emojis["MUTE"], value="mute")
    embed.add_field(name=emojis["UNMUTE"], value="un-mute")
    embed.add_field(name=emojis["DEAFEN"], value="deafen")
    embed.add_field(name=emojis["UNDEAFEN"], value="un-deafen")
    embed.add_field(name=emojis["ALL"], value="mute + deafen")
    embed.add_field(name=emojis["UNALL"], value="un-mute + un-deafen")

    await ctx.respond("React with an emoji below!")

    message = await ctx.send(embed=embed)

    for emoji in emojis.values():
        await message.add_reaction(emoji)
