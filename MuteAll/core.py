import discord
from MuteAll import errors


async def do(ctx, task="mute", members=[]):
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
        return await errors.show_permission_error(ctx)
    except Exception as e:
        return await errors.show_common_error(ctx, e)
