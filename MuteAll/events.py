import discord


async def on_ready(bot):
    activity = discord.Activity(
        name="for slash commands", type=discord.ActivityType.watching)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Logged in as {bot.user}")

# DEPRECATED
# async def on_guild_join(guild):
#     embed = discord.Embed()
#     for channel in guild.text_channels:
#         if channel.permissions_for(guild.me).send_messages:
#             embed.add_field(name="Hey, thanks for adding me!",
#                             value="If you are already in a voice channel, please reconnect everyone. Type `.help` to view all the commands.")
#             await channel.send(embed=embed)
#             break
