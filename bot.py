import aiohttp
import aiosqlite
import asyncio
import discord
from discord.ext import commands
from functools import reduce
import json
import random

__version__ = "0.2"


class PhysBot(commands.Bot):
    """Subclass of the commands.Bot class.
    This is helpful when adding attributes to the bot such as a
    database connection or http session.
    """
    pass


if __name__ == '__main__':
    with open("token.txt") as f:
        TOKEN = f.read()

    bot = PhysBot(
        description="Bot pour le serveur Discord de la PHYSUM!",
        command_prefix="p.",
        activity=discord.Game(name="aider la Physum"),
    )

    startup_extensions = [
        'cogs.memes',
        'cogs.physum',
        'cogs.information',
    ]

    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(TOKEN)
