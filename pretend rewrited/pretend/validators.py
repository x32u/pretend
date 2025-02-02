import json
import emoji
import humanfriendly

from discord.ext import commands
from pretend.lastfmhandler import Handler
from pretend.exceptions import LastFmException, WrongMessageLink

class ValidNickname(commands.Converter):
    async def convert(self, ctx, argument: str):
        if argument.lower() == "none":
            return None
        else:
            return argument
        
class ValidLastFmName(commands.Converter):
    def __init__(self):
        self.lastfmhandler = Handler("43693facbb24d1ac893a7d33846b15cc")

    async def convert(self, ctx, argument: str):
        check = await ctx.bot.db.fetchrow(
            "SELECT username FROM lastfm WHERE user_id = $1", ctx.author.id
        )

        if not await self.lastfmhandler.lastfm_user_exists(argument):
            raise LastFmException("This account **doesn't** exist")

        if check:
            if check[0] == argument:
                raise LastFmException(f"You are **already** registered with this name")
            await ctx.bot.db.execute(
                "UPDATE lastfm SET username = $1 WHERE user_id = $2",
                argument,
                ctx.author.id,
            )
        else:
            await ctx.bot.db.execute(
                """
        INSERT INTO lastfm 
        VALUES ($1,$2,$3,$4,$5)
        """,
                ctx.author.id,
                argument,
                json.dumps(["🔥", "🗑️"]),
                None,
                None,
            )

        return await self.lastfmhandler.get_user_info(argument)