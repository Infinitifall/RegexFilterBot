import discord

import asyncio

from src.regex import regexFilter, updateRe
from src.help import help_message
from data.bot_globals import my_guild_ids, admin_ids, command_prefix, bot_token


client = discord.Client()


@client.event
async def on_ready():
    print("logged in as {} {} ({})".format(client.user.name, client.user.discriminator, client.user.id))
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{command_prefix} help"))


@client.event
async def on_message(message):
    
    if message.guild.id not in my_guild_ids:
        # do nothing
        return

    if (message.author == client.user) or (message.author.bot):
        # if message is by self or by another bot do nothing
        return
    
    print(f"> {message.author.name.rjust(10)}: {message.content}")

    if not message.content.startswith(command_prefix):
        message_re = regexFilter(message)

        if "m" in message_re["action"]:
            myrole = discord.utils.get(message.guild.roles, id=message_re["muterole_id"])
            await message.author.add_roles(myrole)
            print(f"muted: {message.content[:30]}")
        
        if "r" in message_re["action"]:
            mymessage = await message.channel.send(f"{message.author.name} your message has been flagged for reason: `{message_re['description']}`")
            print(f"replied: {message.content[:30]}")
            await asyncio.sleep(5)
            await mymessage.delete()

        if "d" in message_re["action"]:

            if message_re["delay"] > 0:
                print(f"to be deleted in {message_re['delay']}s: {message.content[:30]}")
                await asyncio.sleep(message_re["delay"])
            
            await message.delete()
            print(f"deleted: {message.content[:30]}")
        
        return
    
    message_string = message.content[len(command_prefix):]

    if message_string in {"hello", "hi", "ping", "p"}:
        print("p")
        # not an embed, we want the user to get pinged!
        await message.channel.send(f"{message.author.mention}")
        return

    elif message_string in {"help", "h"}:
        print("h")
        await message.channel.send(embed=discord.Embed(description=help_message, color=0x000000))
        return
    
    elif ((message_string in {"regex", "r"}) and (message.author.id in admin_ids)):
        print("r")
        updateRe()
        return
    
    elif ((message_string in {"regexlist", "rl"}) and (message.author.id in admin_ids)):
        print("rl")
        await message.channel.send(file=discord.File("data/regex_filter.json"))
        return
    
    else:
        await message.channel.send(f"cant recognize or execute command `{message_string}`")
        print(f"cant recognize or execute command {message_string}")
        return



if (__name__ == "__main__"):
    client.run(bot_token)
