from discord.ext import commands
import ping3
import os

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def status(ctx):
    ip = "5.20.187.185:25565"  # change to your server IP
    response = ping3.ping(ip, timeout=2)

    if response:
        await ctx.send("🟢 Online")
    else:
        await ctx.send("🔴 Offline")

bot.run(os.getenv("TOKEN"))