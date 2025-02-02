from structure import Pretend
# from structure.utilities import FMHandler
from structure.managers import Context
from discord import Message, Embed
from discord.ext.commands import Cog, group, command, Context as DefaultContext, MinimalHelpCommand, Bot

class LastFM(Cog):
    def __init__(self, bot: Pretend):
        self.bot: Pretend = bot


async def setup(bot: Pretend) -> None:
    await bot.add_cog(LastFM(bot))
