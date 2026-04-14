import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
import os

# Intents setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load environment variables
TOKEN = os.getenv("TOKEN")
SERVER_IP = os.getenv("SERVER_IP")

if not TOKEN:
    raise ValueError("TOKEN is not set")
if not SERVER_IP:
    raise ValueError("SERVER_IP is not set")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    update_status.start()


@tasks.loop(seconds=30)
async def update_status():
    print("Updating presence...")  # debug

    try:
        server = JavaServer.lookup(SERVER_IP)

        # run blocking call safely
        status = await bot.loop.run_in_executor(None, server.status)

        players = f"{status.players.online}/{status.players.max}"

        await bot.change_presence(
            activity=discord.Game(name=f"🟢 {players} players")
        )

    except Exception as e:
        print(f"Error: {e}")

        await bot.change_presence(
            activity=discord.Game(name="🔴 Server Offline")
        )


@update_status.before_loop
async def before_update():
    await bot.wait_until_ready()


bot.run(TOKEN)
