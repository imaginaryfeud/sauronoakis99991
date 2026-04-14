import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
import os

# Intents setup (required)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load environment variables (from Railway)
TOKEN = os.getenv("TOKEN")
SERVER_IP = os.getenv("SERVER_IP")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Validate variables early
if not TOKEN:
    raise ValueError("TOKEN is not set in Railway variables")
if not SERVER_IP:
    raise ValueError("SERVER_IP is not set in Railway variables")
if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID is not set in Railway variables")

CHANNEL_ID = int(CHANNEL_ID)

last_message = None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    update_status.start()


# 🔧 FIX: wait until bot is ready before loop starts
@update_status.before_loop
async def before_update():
    await bot.wait_until_ready()


@tasks.loop(seconds=30)
async def update_status():
    global last_message

    print("Loop running...")  # DEBUG

    try:
        # 🔧 FIX: fetch channel properly (works on Railway)
        channel = await bot.fetch_channel(CHANNEL_ID)

        server = JavaServer.lookup(SERVER_IP)
        status = server.status()

        players = f"{status.players.online}/{status.players.max}"
        version = status.version.name
        motd = status.description

        message_text = (
            f"🟢 **Online**\n"
            f"Players: {players}\n"
            f"Version: {version}\n"
            f"MOTD: {motd}"
        )

        # Update bot presence
        await bot.change_presence(
            activity=discord.Game(name=f"🟢 {players} players")
        )

    except Exception as e:
        print(f"Error: {e}")  # DEBUG

        message_text = "🔴 **Offline**"

        await bot.change_presence(
            activity=discord.Game(name="🔴 Server Offline")
        )

    # Send or update message
    if last_message is None:
        last_message = await channel.send(message_text)
    else:
        await last_message.edit(content=message_text)


@bot.command()
async def status(ctx):
    await ctx.send("Live status is being updated above 👆")


bot.run(TOKEN)
