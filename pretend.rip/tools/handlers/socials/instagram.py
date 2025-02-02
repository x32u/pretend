from discord.ext import commands
from ...helpers import PretendContext


class InstagramUser(commands.Converter):
    async def convert(self, ctx: PretendContext, argument: str):
        return
