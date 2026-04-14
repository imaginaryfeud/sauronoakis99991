import discord
from discord.ext import commands
from mcstatus import JavaServer
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def status(ctx):
    try:
        server = JavaServer.lookup("5.20.187.185:25565")
        status = server.status()

        await ctx.send(f"🟢 Online - {status.players.online}/{status.players.max} players")
    except:
        await ctx.send("🔴 Offline")

bot.run(os.getenv("TOKEN"))
