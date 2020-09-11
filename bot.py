import aiohttp
import aiosqlite
import asyncio
import discord
from discord.ext import commands
from functools import reduce
import json
import random

__version__ = "0.2"

bot = commands.Bot(command_prefix="p.", activity=discord.Game(name="aider la Physum"))



with open("token.txt") as f:
    TOKEN = f.read()

@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.channels, name="rôles")
    if guild.system_channel is not None:
        to_send = f'Bienvenue {member.mention} dans le serveur de la Physum!\nChoisis ton année et ton programme dans {channel.mention} pour avoir accès à plus de salons et de fun :) '
        await guild.system_channel.send(to_send)

@bot.event
async def on_message(message):
    if message.author.name == "Hassan":
        await message.add_reaction("<:crottesulcoeur:751234270781112420>")
    for forbidden_word in ["ingénieur", "elon musk", "pi=3"]:
        if forbidden_word in message.content.lower():
            await message.add_reaction("\U0001f4a9")
    await bot.process_commands(message)

@bot.group(invoke_without_command=True)
async def conseil(ctx, *mots):
    '''donne un conseil sur ce que vous demandez si disponible'''
    if not len(mots) == 1:
        mot = "".join(mots)

    else:
        mot = mots[0]
    try:
        # version pour  database sqlite3
        #async with aiosqlite.connect("infos.db") as conn:
            #async with conn.cursor() as c:
                #conseil = await c.execute("SELECT * FROM conseil WHERE nom=?",mot)
        #await ctx.send(conseil)
        with open("conseil.json") as json_file:
            data = json.load(json_file)
            info = data[mot]
        if info:
            await ctx.send(info)
    except:
        await ctx.send("désolé, je ne peux pas t'aider :(")

@conseil.command()
async def create(ctx, motclé: str, *conseil):
    # version pour database sqlite3
    #async with aiosqlite.connect("infos.db") as conn:
        #async with conn.cursor() as c:
            #await c.execute("INSERT INTO conseil (nom) VALUES (?)", "".join(conseil))
    with open("conseil.json", "r+") as json_file:
        data = json.load(json_file)
        data[motclé] = " ".join(conseil)
        json_file.seek(0)
        json.dump(data, json_file, indent=4)
        json_file.truncate()

@bot.command()
async def wiki(ctx, *nom_article):
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

@bot.command()
async def meme(ctx, *category):
    '''Trouve un meme (par défaut sur r/physicsmemes) sur le subreddit mentionné'''
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


@bot.command()
async def ménage(ctx, nbr_de_messages):
    pass

bot.run(TOKEN)