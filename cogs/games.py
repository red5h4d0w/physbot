import asyncio
import discord
from discord.ext import commands
import numpy as np
import unidecode
import string

from . import emoji


with open('lexique_physique_filtre.txt', encoding='utf-8') as f:
    WORD_LIST = f.read().split('\n')

CANCEL = [
    'cancel',
    'stop',
]

HANGMAN_LIMBS = [
    [(1, 0), emoji.Hangman.DIZZY_FACE],
    [(1, 1), emoji.Hangman.SHIRT],
    [(1, 2), emoji.Hangman.JEANS],
    [(0, 1), emoji.Hangman.POINT_LEFT],
    [(2, 1), emoji.Hangman.POINT_RIGHT],
    [(0, 3), emoji.Hangman.SHOE],
    [(2, 3), emoji.Hangman.SHOE],
]


class Hangman:
    """Class that contains the Hangman game."""

    def __init__(self, ctx, bot):
        self.ctx = ctx
        self.bot = bot
        word, url = np.random.choice(WORD_LIST).split(', ')
        # word, url = WORD_LIST[49].split(', ')
        self.word_undecoded = word
        self.word_to_guess = unidecode.unidecode(word).lower()
        self.word_url = url
        self.chances = len(HANGMAN_LIMBS)
        # self.won = False
        self.bad_guesses = []
        self.good_guesses = []

        self.embed = discord.Embed(
            title=None,
            color=np.random.randint(0xFFFFFF),  # Random color
        ).set_author(
            name=self.ctx.author.display_name,
            icon_url=self.ctx.author.avatar_url_as(static_format='png'),
        ).add_field(
            name='Pendu',
            value=None,  # will be filled later
            inline=True,
        ).add_field(
            name='Mauvaises lettres',
            value=None,
            inline=True,
        ).add_field(
            name='Devine le mot!',
            value='Aucune',  # will be filled after
            inline=False,
        )

    async def play(self):
        """Play a game of Hangman!"""

        def check(message):
            valid = (
                message.author == self.ctx.author
                and message.channel == self.ctx.channel
                and (
                    len(message.content) == 1
                    or message.content.lower() in CANCEL
                )
            )
            return valid

        hint_message = "Devine le mot! Entre une lettre pour commencer."
        self.update_embed(hint_message)
        self.message_game = await self.ctx.send(embed=self.embed)

        while self.chances > 0 and not self.won:

            try:
                guess_message = await self.bot.wait_for(
                    'message',
                    timeout=5 * 60,  # 5 minutes
                    check=check,
                )
            except asyncio.TimeoutError:
                # we don't want games to run indefinetly
                break

            guess = guess_message.content.lower()
            await guess_message.delete(delay=1)

            if guess.lower() in CANCEL:
                break

            elif guess not in string.ascii_lowercase:
                hint_message = "Entre une seule lettre s'il te plaît."

            elif guess in self.good_guesses + self.bad_guesses:
                hint_message = "Tu as déjà essayé cette lettre."

            elif guess not in self.word_to_guess:
                self.chances -= 1
                self.bad_guesses.append(guess)
                hint_message = "Non, désolé! Essaie une autre lettre."

            else:
                self.good_guesses.append(guess)
                hint_message = "Correct! Essaie une autre lettre."

            # self.won = all([x in self.good_guesses
            #                 for x in set(self.word_to_guess)])

            if not self.won and self.chances > 0:
                self.update_embed(hint_message)
                await self.message_game.edit(embed=self.embed)

        if self.won:
            hint_message = (
                f"Tu as gagné! Le mot était [{self.word_undecoded}]"
                f"({self.word_url})."
            )
        else:
            hint_message = (
                f'Tu as perdu! Le mot était [{self.word_undecoded}]'
                f'({self.word_url}).'
            )

        self.update_embed(hint_message)
        await self.message_game.edit(embed=self.embed)

    @property
    def won(self):
        won = True
        for x in set(self.word_to_guess):
            if x in string.punctuation or x in string.whitespace:
                # ignore punctuation and whitespaces
                # ie in composite words 'moment angulaire' or
                # 'photo-ionisation'
                continue
            won = won and x in self.good_guesses

        return won

    def update_embed(self, hint_message):
        """Edit the Embed, the progress on the word to guess, chances,
        and the graphics of the hangman.
        """
        characters = []
        for x in self.word_to_guess:
            if x in string.ascii_lowercase:
                if x in self.good_guesses:
                    character = emoji.Alphabet[x.upper()]
                else:
                    character = emoji.Hangman.BLANK

            else:
                character = x

            characters.append(str(character))

        current_progress = '\U000000A0'.join(characters)

        bad_guesses_str = ' '.join(c.upper() for c in self.bad_guesses)
        # if it is an empty string, the Embed will complain
        if not bad_guesses_str:
            bad_guesses_str = None

        graphics = self.make_graphics(len(self.bad_guesses))
        graphics_str = '\n'.join(''.join(line) for line in graphics.T)

        self.embed.set_field_at(
            index=0,  # graphics
            name=self.embed.fields[0].name,
            value=graphics_str,
            inline=self.embed.fields[0].inline,
        ).set_field_at(
            index=1,  # bad guesses
            name=self.embed.fields[1].name,
            value=bad_guesses_str,
            inline=self.embed.fields[1].inline,
        ).set_field_at(
            index=2,  # word to guess
            name=self.embed.fields[2].name,
            value=current_progress,
            inline=self.embed.fields[2].inline,
        )

        self.embed.description = hint_message

    def make_graphics(self, number_bad_guesses):
        """Return an array for the hangman picture with the correct limbs
        displayed according to the number bad guesses made.
        """
        if number_bad_guesses == 0:
            return np.full((3, 4), str(emoji.Hangman.BLACK))
        else:
            limb = HANGMAN_LIMBS[number_bad_guesses - 1]
            graphics = self.make_graphics(number_bad_guesses - 1)
            graphics[limb[0]] = str(limb[1])
            return graphics


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hangman'])
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def pendu(self, ctx):
        """Joue une partie de pendu à thématique physique."""

        game = Hangman(ctx, self.bot)
        await game.play()

    @pendu.error
    async def hangman_error(self, ctx, error):
        """Error handler for the hangman command."""

        if isinstance(error, commands.MaxConcurrencyReached):
            error_msg = await ctx.send(
                "Seulement une partie de pendu peut être active à la fois")
            await ctx.message.delete()
            await asyncio.sleep(5)
            await error_msg.delete()


def setup(bot):
    bot.add_cog(Games(bot))
