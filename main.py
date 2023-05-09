import os
import discord
import asyncio
from discord.ext import commands


bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


async def main():
    async with bot:
        await bot.load_extension("task_handler")
        await bot.start(os.environ['discord_key'])

asyncio.run(main())
