import discord
from discord.ext import commands
import configparser
import os
import datetime

version = 0.1
print('##########################')
print('# Discord WatchBot       #')
print(f'# Version {version}            #')
print('##########################')
print('\n')

CONFIG_DIR = "config"
DB_FILE = "./config/DATABASE.db"
CONFIG_FILE = "config/config.ini"
config = configparser.ConfigParser()

##### CONFIG HANDELING #####
if not os.path.exists(CONFIG_DIR):
    print("Creating CONFIG_DIR\n")
    os.system(f"mkdir {CONFIG_DIR}")
if not os.path.exists(CONFIG_FILE):
    print("Creating CONFIG_FILE \n")
    config.add_section("Settings")
    config.set("Settings", "TOKEN", "")
    config.set("Settings", "BOT_PREFIX", "!")
    config.set("Settings", "OWNER_ID", "150933142482452480")
    config.add_section("Subscribers")
    config.set("Subscribers", "USERs", "")
    config.add_section("Observed")
    config.set("Observed", "BOTs", "")
    file = open(CONFIG_FILE, 'w')
    config.write(file)
    file.close()
else:
    print("All Direcories and Files in place!\nContinuing")


config.read(CONFIG_FILE)
BOT_PREFIX = config.get('Settings', 'BOT_PREFIX')
TOKEN = config.get('Settings', 'TOKEN')
if TOKEN == "" or TOKEN == None:
    print("##### Please edit the settings-file and fill in a Bot-Token #####")
    exit()
else:
    TOKEN = config.get("Settings", "TOKEN")
    BOT_PREFIX = config.get("Settings", "BOT_PREFIX")
    OWNER_ID = config.get("Settings", "OWNER_ID")
    USERS = config.get("Subscribers", "USERs").split()
    BOTS = config.get("Observed", "BOTs").split()

##### COLORS #####
RED = 0xe91e63
GREEN = 0x2ecc71

class NOTIFY:
    async def notify_user(user_id: int, title: str, name: str, content: str, colour: int, thumbnail: str):
        user = client.get_user(int(user_id))
        embed = discord.Embed(title=title, colour=colour)
        embed.add_field(name=name, value=content, inline=True)
        embed.set_thumbnail(url=thumbnail)
        embed.timestamp = datetime.datetime.utcnow()
        await user.send(embed=embed)

    async def notify_announcement_channel(channel_id: int, title: str, content: str):
        notify_announcement_channel = client.get_channel(channel_id)
        embed = discord.Embed(title="Update 🔔", colour=0xff0000)
        embed.add_field(name=title, value=content, inline=True)
        embed.timestamp = datetime.datetime.utcnow()
        await notify_announcement_channel.send(embed=embed)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = commands.Bot(command_prefix=BOT_PREFIX, intents=discord.Intents.all(), case_insensitive=True,
                          owner_id=OWNER_ID)
    #slash = SlashCommand(client, sync_commands=True)


    @client.event
    async def on_ready():
        print("Successfully logged in as {0.user}".format(client))
        print(f"Discord.py version: {discord.__version__}")
        print(f"Name: {client.user.name}")
        print(f"ID: {client.user.id}")
        print(f"Prefix: {BOT_PREFIX}")
        print(
            f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=261993005047&scope=bot%20applications.commands")
        print("--------------------------------------------------")
        game = discord.Game("/help")
        await client.change_presence(status=discord.Status.offline)

    @client.event
    async def on_member_update(before, after):
        if before.bot == True:
            print("MEMBER UPDATE")
            print(f"{datetime.datetime.utcnow()} - Status-ÄNDERUNG \nUser: {before} Status: {before.status} --> User: {after} Status: {after.status}")
            for filter_user in BOTS:
                if int(filter_user) == before.id:
                    if str(after.status) == "offline":
                        for i in USERS:
                            await NOTIFY.notify_user(int(i), "‼️ STATUS NOTIFICATION ‼️", f"User: {after}",
                                                    f"**Status: *{after.status}***", RED, before.avatar_url)
                    elif str(after.status) == "online":
                        pass
                        """
                        await NOTIFY.notify_user(150933142482452480, "🔔 STATUS NOTIFICATION 🔔", f"User: {after}",
                                                 f"**Status: *{after.status}***",
                                                 GREEN, before.avatar_url)
                        """

                    else:
                        pass
                else:
                    pass
        else:
            pass

client.run(TOKEN)
