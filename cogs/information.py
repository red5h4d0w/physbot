import aiohttp
import json
from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def conseil(self, ctx, *mots):
        '''donne un conseil sur ce que vous demandez si disponible'''
        if not len(mots) == 1:
            mot = "".join(mots)

        else:
            mot = mots[0]
        try:
            # version pour  database sqlite3
            # async with aiosqlite.connect("infos.db") as conn:
            #     async with conn.cursor() as c:
            #         conseil = await c.execute("SELECT * FROM conseil WHERE nom=?",mot)
            # await ctx.send(conseil)
            with open("conseil.json") as json_file:
                data = json.load(json_file)
                info = data[mot]
            if info:
                await ctx.send(info)
        except:
            await ctx.send("désolé, je ne peux pas t'aider :(")

    @conseil.command(name='create')
    async def conseil_create(self, ctx, motclé: str, *conseil):
        # version pour database sqlite3
        # async with aiosqlite.connect("infos.db") as conn:
        #     async with conn.cursor() as c:
        #         await c.execute("INSERT INTO conseil (nom) VALUES (?)", "".join(conseil))
        with open("conseil.json", "r+") as json_file:
            data = json.load(json_file)
            data[motclé] = " ".join(conseil)
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()

    @commands.command()
    async def wiki(self, ctx, *nom_article):
        if not len(nom_article) == 1:
            url = "http://fr.wikipedia.org/wiki/" + nom_article[0].capitalize() + "_" +"_".join(nom_article[1:])
        else:
            url = "http://fr.wikipedia.org/wiki/" + nom_article[0].capitalize()
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                if request:
                    await ctx.send(url)
                else:
                    await ctx.send("Désolé, je n'ai pas réussi à trouver l'article")


def setup(bot):
    bot.add_cog(Information(bot))
