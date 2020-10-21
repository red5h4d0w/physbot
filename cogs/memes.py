import aiohttp
from discord.ext import commands
import random


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if "<:ripsimon:768530426884915272>" in message.content:
            await message.add_reaction("<:faridsus:768530389685764127>")

        if message.author.name == "Hassan":
            await message.add_reaction("<:crottesulcoeur:751234270781112420>")

        for forbidden_word in ["ingénieur", "elon musk", "pi=3"]:
            if forbidden_word in message.content.lower():
                await message.add_reaction("\U0001f4a9")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction) == "<:ripsimon:768530426884915272>":
            await reaction.message.add_reaction("<:faridsus:768530389685764127>")

    @commands.command()
    async def meme(self, ctx, *category):
        '''Trouve un meme sur le subreddit mentionné
        (par défaut sur r/physicsmemes)
        '''
        if not category:
            category = ["physicsmemes"]

        subreddit = "".join(category).lower()
        url = "http://www.reddit.com/r/" + subreddit + "/hot/.json?limit=50"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                if request:
                    json = await request.json()
                else:
                    await ctx.send("Je n'ai pas réussi")
        posts = json["data"]["children"]
        post = random.choice(posts)
        img = post["data"]["url"]
        await ctx.send(img)


def setup(bot):
    bot.add_cog(Memes(bot))
