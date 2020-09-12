from discord.ext import commands


class Admin(commands.Cog):
    """Administration commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permission(administrator=True)
    async def remove(self, ctx, number_of_messages: int):
        """Remove a given amount of messages."""

        # TODO: have a check that will not remove messages from Admins
        deleted = await ctx.channel.purge(limit=number_of_messages)
        await ctx.send(
            f"J'ai effacé {len(deleted)} messages dans {ctx.channel.mention}"
        )


def setup(bot):
    bot.add_cog(Admin(bot))