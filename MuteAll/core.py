import discord
from MuteAll import errors


async def do(ctx, task="mute", members=[]):

    try:

        for member in members:

            match task:
                case "mute":
                    if member.bot:
                        await member.edit(mute=False)
                    else:
                        await member.edit(mute=True)
                case "unmute":
                    if member.bot:
                        await member.edit(mute=True)
                    else:
                        await member.edit(mute=False)
                case "end":
                    await member.edit(mute=False)
                case "deafen":
                    await member.edit(deafen=True)
                case "undeafen":
                    await member.edit(deafen=False)
                case "all":
                    if member.bot:
                        await member.edit(mute=False)
                    else:
                        await member.edit(mute=True)
                    await member.edit(deafen=True)
                case "unall":
                    if member.bot:
                        await member.edit(mute=True)
                    else:
                        await member.edit(mute=False)
                    await member.edit(deafen=False)

            await ctx.message.add_reaction("👌")

    except discord.Forbidden:  # the bot doesn't have the permission to mute
        return await errors.show_permission_error(ctx)
    except Exception as e:
        return await errors.show_common_error(ctx, e)
