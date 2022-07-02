def get_emojis(bot):
    emojis = {}

    emojis["MUTE"] = bot.get_emoji(992824561915670669)
    emojis["UNMUTE"] = bot.get_emoji(992824559596224574)
    emojis["DEAFEN"] = bot.get_emoji(992824555691327508)
    emojis["UNDEAFEN"] = bot.get_emoji(992824557868175360)
    emojis["ALL"] = bot.get_emoji(992824551077580850)
    emojis["UNALL"] = bot.get_emoji(992824552876953641)

    return emojis
