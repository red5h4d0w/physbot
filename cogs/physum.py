import discord
from discord.ext import commands


class Physum(commands.Cog):
    """Utilities for the PHYSUM Discord Server."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel = discord.utils.get(guild.channels, name="rôles")
        if guild.system_channel is not None:
            to_send = (
                f'Bienvenue {member.mention} dans le serveur de la Physum!\n'
                f'Choisis ton année et ton programme dans {channel.mention} '
                'pour avoir accès à plus de salons et de fun :) '
            )
            await guild.system_channel.send(to_send)


def setup(bot):
    bot.add_cog(Physum(bot))
