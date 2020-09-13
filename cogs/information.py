import aiohttp
import aiosqlite
from discord.ext import commands, tasks


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._create_tables.start()

    @commands.group(invoke_without_command=True)
    async def conseil(self, ctx, *, mots: str):
        '''donne un conseil sur ce que vous demandez si disponible'''

        row = await self._get_conseil(mots)
        if row is None:
            await ctx.send("Il n'y a pas de conseil sous cette clé.")

        else:
            await ctx.send(row['conseil'])

    @conseil.command(name='create')
    async def conseil_create(self, ctx, motclé: str, *, conseil: str):
        """Subcommande pour créer un nouveau conseil."""

        await self._save_conseil(ctx, motclé, conseil)

        await ctx.send(
            f"OK! J'ai enregistré le conseil sous la clé `{motclé}`.")

    @conseil_create.error
    async def conseil_create_error(self, ctx, _error):
        """Error handler for the conseil_create command."""

        error = getattr(_error, 'original', _error)

        if isinstance(error, aiosqlite.IntegrityError):
            await ctx.send("Il y a déjà un conseil avec cette clé.")

        else:
            raise _error

    # TODO: conseil_delete, conseil_update commands

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

    @tasks.loop(count=1)
    async def _create_tables(self):
        """Crée les tables nécessaires, si elles n'existent pas déjà."""

        await self.bot.db.execute(
            """
            CREATE TABLE IF NOT EXISTS information_conseil(
                conseil    TEXT      NOT NULL,
                created_at TIMESTAMP NOT NULL,
                key        TEXT      NOT NULL UNIQUE,
                user_id    INTEGER   NOT NULL
            )
            """
        )

        await self.bot.db.commit()

    async def _get_conseil(self, key):
        """Cherche le conseil avec la clé 'key' dans la base de données.
        Peut retourner None si la clé n'existe pas.
        """
        async with self.bot.db.execute(
                """
                SELECT *
                  FROM information_conseil
                 WHERE key = :key
                """,
                {'key': key}
        ) as c:
            row = await c.fetchone()

        return row

    async def _save_conseil(self, ctx, key, conseil):
        """Enregistre le conseil dans la base de données."""

        await self.bot.db.execute(
            """
            INSERT INTO information_conseil
            VALUES (:conseil,
                    :created_at,
                    :key,
                    :user_id)
            """,
            {
                'conseil': conseil,
                'created_at': ctx.message.created_at,
                'key': key,
                'user_id': ctx.author.id,
            }
        )

        await self.bot.db.commit()


def setup(bot):
    bot.add_cog(Information(bot))
