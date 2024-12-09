import discord
from discord.ext import commands
import asyncio
import json
from commands.Ping import PingCog
from commands.Team_By_Name_Command import TeamByNameCog

with open("bot.json") as botFile:
    bot = json.load(botFile)
    botFile.close()

token =   bot["token"]
clientid = bot["clientID"]
prefix = "!!"

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.guild_messages = True
intents.message_content = True
client = commands.Bot(command_prefix=prefix, intents=intents, help_command=None, application_id=clientid)

@client.event
async def on_ready():
    print("Bot is online")
    print(f"Logged in as: {client.user} - {client.user.id}")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@client.event
async def on_guild_join(guild: discord.Guild):  
    await client.tree.sync(guild=guild)

async def setup_hook():
    logs = await client.tree.sync()
    print(f"[!] Synced {len(logs)} app_commands")

async def load_cogs():
    cogs_to_load = [
        PingCog(client),
        TeamByNameCog(client)
    ]
    for cog in cogs_to_load:
        await client.add_cog(cog)

# Load cogs before starting the bot
async def startup():
    await load_cogs()

# Run the bot
asyncio.run(startup())
client.run(token)