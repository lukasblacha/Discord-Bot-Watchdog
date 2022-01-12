import discord
import slash as slash
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand, ComponentContext
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component, create_select, \
    create_select_option
from discord_slash.model import ButtonStyle, SlashCommandPermissionType
import configparser
import os
import datetime

version = 0.1
print('##########################')
print('# Discord WatchBot       #')
print(f'# Version {version}            #')
print('##########################')
print('\n')

DB_FILE = "./config/DATABASE.db"
CONFIG_FILE = "config/settings.ini"
config = configparser.ConfigParser()

##### CONFIG HANDELING #####
if os.path.exists(CONFIG_FILE):
    pass
else:
    print("Creating config-file \n")
    config.add_section("Settings")
    config.set("Settings", "TOKEN", "")
    config.set("Settings", "BOT_PREFIX", "!")
    config.set("Settings", "OWNER_ID", "")
    file = open(CONFIG_FILE, 'w')
    config.write(file)
    file.close()

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

##### COLORS #####
RED = 0xe91e63
GREEN = 0x2ecc71

class NOTIFY:
    #User mention with <@ID>, Role mention with <@&ID>
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
    slash = SlashCommand(client, sync_commands=True)


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
        await client.change_presence(status=discord.Status.online, activity=game)

    @client.event
    async def on_member_update(before, after):
        print("MEMBER UPDATE")
        print(f"Status-ÄNDERUNG \nUser: {before} Status: {before.status} --> User: {after} Status: {after.status}")
        print(f"User is Bot: {before.bot}")
        if before.id == 411798936643436545:
            if str(after.status) == "offline":
                await NOTIFY.notify_user(150933142482452480, "‼️ STATUS NOTIFICATION ‼️", f"User: {after}",
                                         f"**Status: *{after.status}***",
                                         RED, before.avatar_url)
            else:
                await NOTIFY.notify_user(150933142482452480, "🔔 STATUS NOTIFICATION 🔔", f"User: {after}",
                                         f"**Status: *{after.status}***",
                                         GREEN, before.avatar_url)
        else:
            pass


    @slash.slash(name="watchbot", description="Shows the available WatchBot commands", options=[
        create_option(
            name="farbe",
            description="Gib deinem Team eine Farbe",
            option_type=6,
            required=True,
            choices=[
                create_choice(
                    name="Smaragt Grün",
                    value="0x1abc9c")
            ]
        )
    ]
                 )
    async def _watchbot(ctx, watch, unwatch):
        await ctx.send("TEST Message", hidden=True)
        if watch != None:
            print(watch)
        elif unwatch != None:
            print(unwatch)
        else:
            pass

client.run(TOKEN)
