from structure import Pretend
from structure.utilities import dump, Snipe
from structure.managers import Context
from random import choice
from time import time
from discord import Message, Embed
from discord.ext.commands import Cog, command, has_permissions
import humanize
from xxhash import xxh32_hexdigest
import datetime

class Miscellaneous(Cog):
    def __init__(self, bot: Pretend):
        self.bot: Pretend = bot


    @command(
        name="ping",
        description="View the bot's latency.",
    )
    async def ping(self, ctx: Context) -> Message:
        """
        View the bot's latency and make a random funny reference.
        """
        ping_responses = [
            "your mother",
            "the chinese government",
            "lastfm's ass computers",
            "my teeshirt",
            "lil mosey",
            "north korea",
            "localhost",
            "twitter",
            "the santos",
            "the trash",
            "a connection to the server",
            "four on twitter",
            "6ix9ine's ankle monitor",
            "fivem servers",
            "new york",
            "my black airforces",
            "netflix database"
        ]

        start = time()
        message = await ctx.send(content="...")
        finished = time() - start

        # Create the embed
        embed = Embed(
            description=(
                f"It took `{int(self.bot.latency * 1000)}ms` to ping **{choice(ping_responses)}**\n"
                f"Edit: `{finished:.2f}ms`."
            ),
            color=0x2b2d31  
        )

        return await message.edit(content=None, embed=embed)

async def setup(bot: Pretend) -> None:
    await bot.add_cog(Miscellaneous(bot))
