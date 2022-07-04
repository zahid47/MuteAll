async def show_common_error(ctx, e):
    await ctx.respond(f"Something went wrong ({e})", value="[Join support server](https://discord.gg/8hrhffR6aX) for help.")


async def show_permission_error(ctx):
    await ctx.respond("Please make sure I have the necessary permissions. If unsure, try giving me the `administrator` permission or [Join support server](https://discord.gg/8hrhffR6aX) for more help")

# async def report_common_error(ctx, bot, e):
#     await ctx.respond(f"Something went wrong, I've notified the admins.", value="[Join support server](https://discord.gg/8hrhffR6aX) for help.")

#     async def report_to_me(bot, message):
#         user = await bot.fetch_user(187568903084441600)
#         await user.send(message)

#     await report_to_me(bot, e)
