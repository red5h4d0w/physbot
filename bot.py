import aiosqlite
import discord
from discord.ext import commands

__version__ = "0.2"


async def create_db_connection(db_name):
    """Create the connection to the database."""

    return await aiosqlite.connect(
        db_name, detect_types=1)  # 1: parse declared types


class PhysBot(commands.Bot):
    """Subclass of the commands.Bot class.
    This is helpful when adding attributes to the bot such as a
    database connection or http session.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make DB connection, save in memory if no name is provided
        self.db = self.loop.run_until_complete(
            create_db_connection(kwargs.get('db_name', ':memory:')))
        # allow for name-based access of data columns
        self.db.row_factory = aiosqlite.Row

    async def close(self):
        """Close the DB connection and HTTP session."""

        await self.db.close()
        await super().close()


if __name__ == '__main__':
    with open("token.txt") as f:
        TOKEN = f.read()

    bot = PhysBot(
        description="Bot pour le serveur Discord de la PHYSUM!",
        command_prefix="p.",
        activity=discord.Game(name="aider la Physum"),
        db_name='physbot.db',
    )

    startup_extensions = [
        'cogs.memes',
        'cogs.physum',
        'cogs.information',
    ]

    for extension in startup_extensions:
        bot.load_extension(extension)

    bot.run(TOKEN)
