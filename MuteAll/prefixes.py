# DEPRECATED

# import pymongo
# import os

# # DB Setup #############################
# cluster = pymongo.MongoClient(os.getenv("MONGO_STRING"))
# db = cluster["MuteAll"]
# prefixes_collection = db["prefixes"]
# ########################################


# def get_prefix(_, message):

#     if not message.guild:
#         return "."

#     try:
#         result = prefixes_collection.find_one({"_id": message.guild.id})
#         return result["prefix"]

#     except:
#         return "."


# async def changeprefix(ctx, prefix):
#     if not ctx.author.guild_permissions.administrator:
#         return await ctx.send("You need to be an administrator to run this command")

#     server_id = ctx.guild.id

#     if prefix == ".":
#         # default prefix, delete it from db
#         # but what if some dummy wants to change prefix to "." even if its already the default? hmmmm just try except and call it a day ig lol
#         try:
#             prefixes_collection.delete_one({"_id": server_id})
#         except:
#             pass  # ignore lol
#         await ctx.send(f"Prefix changed to {prefix}")

#     elif prefixes_collection.find_one({"_id": server_id}) != None:
#         # already exists, need to update instead
#         prefixes_collection.update_one(
#             {"_id": server_id}, {"$set": {"prefix": prefix}})
#         await ctx.send(f"Prefix changed to {prefix}")

#     else:
#         # add the prefix into the db
#         prefixes_collection.insert_one({"_id": server_id, "prefix": prefix})
#         await ctx.send(f"Prefix changed to {prefix}")


# async def viewprefix(ctx):
#     server_id = ctx.guild.id
#     try:
#         prefix = prefixes_collection.find_one({"_id": server_id})['prefix']
#     except:
#         prefix = "."
#     await ctx.send(f"your prefix is {prefix}")
