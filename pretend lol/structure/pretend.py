import discord_ios
from structure.patcher import interaction
from structure.ext import Client
from structure.config import PRETEND
from structure.managers import ClientSession, ratelimiter, Context, logger as logging, Help, database

from discord import (
    AllowedMentions,
    Intents,
    Message,
    Message,
    HTTPException,
    Embed,
)
from discord.ext.commands import (
    BadLiteralArgument,
    Bot,
    CommandError,
    CommandNotFound,
    CommandOnCooldown,
    MissingPermissions,
    MissingRequiredArgument,
    MissingRequiredFlag,
    NotOwner,
    UserInputError,
)

logger = logging.getLogger(__name__)
from .helpers import (
    Cache
)
from os import environ
from pathlib import Path
from discord.utils import utcnow
from datetime import datetime
from typing import Optional 
from aiohttp.client_exceptions import ClientConnectorError, ClientResponseError
from contextlib import suppress

environ["JISHAKU_HIDE"] = "True"
environ["JISHAKU_RETAIN"] = "True"
environ["JISHAKU_NO_UNDERSCORE"] = "True"
environ["JISHAKU_SHELL_NO_DM_TRACEBACK"] = "True"

class Pretend(Bot):
    def __init__(self: "Pretend"):
        super().__init__(
            auto_update=False,
            help_command=Help(bot=Bot),
            command_prefix=",",
            intents=Intents.all(),
            case_insensitive=True,
            owner_ids=PRETEND.owners,
            allowed_mentions=AllowedMentions(
                replied_user=False,
                everyone=False,
                roles=False,
                users=True,
            ),
        )
        self.session: ClientSession
        self.ext = Client(self)
        self.cache = Cache()
        self.uptime: datetime = utcnow()
        self.logger = logger
        self.color = 0x729BB0
        self.run(PRETEND.token, log_handler=None)

    async def setup_hook(self: "Pretend"):
        self.session = ClientSession()
        self.db = await database.connect()

        await self.load_extension("jishaku")

        for cog in Path("features").glob("**/*.py"):
            *tree, _ = cog.parts
            module = ".".join(tree)
            await self.load_extension(f"{module}.{cog.stem}")

    async def on_ready(self: "Pretend"):
        self.logger.info(f"Logged in as {self.user.name} with {len(set(self.walk_commands())) - 37} commands and {len(self.cogs) - 1} cogs loaded!")
    
    async def process_commands(
        self: "Blare",
        message: Message
    ):
        if not message.guild:
            return

        elif ratelimiter(bucket=f"ratelimit:{message.author.id}", key=message.author.id, rate=3, per=5):
            return

        return await super().process_commands(message)

    async def on_message_edit(
        self: "Pretend", 
        before: Message, 
        after: Message
    ):
        if before.content == after.content:
            return

        await self.on_message(after)

    async def get_context(
        self: "Pretend", 
        message: Message, 
        *, cls=Context
    ) -> Context:
        return await super().get_context(message, cls=cls)

    async def on_command(
        self: "Pretend", 
        ctx: Context
    ):
        self.logger.info(f"{ctx.author} ({ctx.author.id}) executed {ctx.command} in {ctx.guild} ({ctx.guild.id}).")

    async def on_command_error(
        self: "Pretend", 
        ctx: Context, 
        exception: CommandError
    ) -> Optional[Message]:

        exception = getattr(exception, "original", exception)
        if type(exception) in (
            NotOwner,
            CommandNotFound,
            CommandOnCooldown,
            UserInputError
        ):
            return
        
        elif isinstance(
            exception, (
                MissingRequiredArgument, 
                MissingRequiredFlag, 
                BadLiteralArgument
            )
        ):
            return await ctx.send_help(ctx.command)
        
        elif isinstance(exception, MissingPermissions):
            missing_perms = ', '.join(permission for permission in exception.missing_permissions)
    
            return await ctx.alert(f"You are **missing** the following permission: `{missing_perms}`")

        elif isinstance(exception, (CommandError)):
            return await ctx.alert(exception.message)
            
        elif isinstance(exception, ClientConnectorError):
            return await ctx.alert("The API has timed out!")

        elif isinstance(exception, ClientResponseError):
            return await ctx.send(exception.status)

    def check_message(
        self: "Pretend", 
        message: Message
    ) -> bool:
        if not self.is_ready() or message.author.bot or not message.guild:
            return False

        return True
    
    async def on_message(self, message: Message) -> None:
        if not self.check_message(message):
            return
        else:
            await self.process_commands(message)

        if message.content == f"<@{self.user.id}>":
            with suppress(HTTPException):
                prefixes = await self.get_prefix(message)
                prefix = prefixes[0] if isinstance(prefixes, list) else prefixes  
                
                embed = Embed(
                    description=f"Your prefix is `{prefix}`",
                    color=self.color
                )

                await message.reply(embed=embed)
