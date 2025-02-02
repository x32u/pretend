import string
import random
import os
import dotenv
import urllib
import asyncio
import asyncpg
import logging
import discord
import datetime
import colorgram
import json
import aiohttp
from PIL import Image
from typing import Any, List, Union, Optional, Set
from copy import copy

from num2words import num2words
from humanize import precisedelta

from discord.gateway import DiscordWebSocket

from .persistent.vm import VoiceMasterView
from .persistent.tickets import TicketView
from .persistent.giveaway import GiveawayView

from .helpers import (
    PretendContext,
    identify,
    guild_perms,
    CustomInteraction,
    AntinukeMeasures,
    Cache,
)

from .misc.session import Session
from .misc.tasks import (
    pomelo_task,
    snipe_delete,
    shit_loop,
    bump_remind,
#    check_monthly_guilds,
    gw_loop,
    reminder_task,
    counter_update,
)

from .handlers.embedbuilder import EmbedScript

from io import BytesIO

from cogs.music import Music
from cogs.logging import UserBan, LogsView

from concurrent.futures import ThreadPoolExecutor

from discord.ext import commands

from tools.helpers import PretendHelp

dotenv.load_dotenv(verbose=True)

handler = logging.FileHandler(
    filename="discord.log",
    encoding="utf-8",
    mode="w",
)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)  # Changed to DEBUG

formatter = logging.Formatter(
    "%(asctime)s | %(name)-12s: %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S"
)

console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set the logger level to DEBUG

intents = discord.Intents.all()
intents.presences = False

commands.has_guild_permissions = guild_perms
DiscordWebSocket.identify = identify
discord.Interaction.warn = CustomInteraction.warn
discord.Interaction.approve = CustomInteraction.approve
discord.Interaction.error = CustomInteraction.error


class Record(asyncpg.Record):

    def __getattr__(self, name: str):
        return self[name]


class Pretend(commands.AutoShardedBot):
    def __init__(self, db: asyncpg.Pool = None):
        super().__init__(
            command_prefix=getprefix,
            intents=intents,
            help_command=PretendHelp(),
            owner_ids=[
                1327020433740009572, # marian
                1327020433740009572, # karlo
            ],
            case_insensitive=True,
            chunk_guilds_at_startup=False,
            strip_after_prefix=True,
            enable_debug_events=True,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=False, replied_user=False
            ),
            member_cache=discord.MemberCacheFlags(joined=True, voice=True),
            activity=discord.CustomActivity(
                name=";invite - pretend.rip ",
            ),
        )

        self.db = db
        self.avqueue = []
        
        self.login_data = {
            x: os.environ[x] for x in ["host", "password", "database", "user", "port"]
        }
        self.login_data["record_class"] = Record
        
        self.warning = "<:warn:1251929429165477948>"
        self.no = "<:deny:1251929424777969797>"
        self.yes = "<:check:1251929419795398708>"
        
        self.y_color = 0x48DB01
        self.n_color = 0xFC341B
        self.w_color = 0xEFBC1B
        self.color = 0x999999

        self.yes_color = 0x48DB01
        self.no_color = 0xFC341B
        self.w_color = 0xEFBC1B
        
        self.time = datetime.datetime.now()

        self.mcd = commands.CooldownMapping.from_cooldown(
            4, 5, commands.BucketType.user
        )
        self.ccd = commands.CooldownMapping.from_cooldown(
            4, 5, commands.BucketType.channel
        )
        
        self.session = Session()
        self.cache = Cache()
        self.proxy_url = "http://dtgrlmjf-rotate:1fdremd0chpp@p.webshare.io:80"
        
        self.other_bots = {}
        
        self.an = AntinukeMeasures(self)
        self.embed_build = EmbedScript()
        
        self.pfps_send = True
        self.banners_send = True
        
        self.executor = ThreadPoolExecutor(max_workers=3)

    def run(self):
        """
        Run the bot
        """

        return super().run(os.environ["token"], log_handler=handler)

    def ordinal(self, number: int) -> str:
        """
        convert a number to an ordinal number (ex: 1 -> 1st)
        """

        return num2words(number, to="ordinal_num")

    @property
    def public_cogs(self) -> List[commands.Cog]:
        """
        the cogs that are shown in the help command
        """

        return [
            c
            for c in self.cogs
            if not c in ["Jishaku", "Owner", "Members", "Auth", "Reactions", "Messages", "Tasks"]
        ]

    @property
    def uptime(self) -> str:
        """
        The amount of time the bot is running for
        """

        return precisedelta(self.time, format="%0.0f")

    @property
    def chunked_guilds(self) -> int:
        """
        Returns the amount of chunked servers
        """

        return len([g for g in self.guilds if g.chunked])

    @property
    def lines(self) -> int:
        """
        Return the code's amount of lines
        """

        lines = 0
        for d in [x[0] for x in os.walk("./") if not ".git" in x[0]]:
            for file in os.listdir(d):
                if file.endswith(".py"):
                    lines += len(open(f"{d}/{file}", "r").read().splitlines())

        return lines

    def humanize_date(self, date: datetime.datetime) -> str:
        """
        Humanize a datetime (ex: 2 days ago)
        """

        if date.timestamp() < datetime.datetime.now().timestamp():
            return f"{(precisedelta(date, format='%0.0f').replace('and', ',')).split(', ')[0]} ago"
        else:
            return f"in {(precisedelta(date, format='%0.0f').replace('and', ',')).split(', ')[0]}"

    async def dominant_color(self, url: Union[discord.Asset, str]) -> int:
        """
        Get the dominant color of a discord asset or image link
        """

        if isinstance(url, discord.Asset):
            url = url.url

        img = Image.open(BytesIO(await self.session.get_bytes(url)))
        img.thumbnail((100, 100))

        colors = await self.loop.run_in_executor(
            self.executor, colorgram.extract, img, 1
        )

        return discord.Color.from_rgb(*list(colors[0].rgb)).value

    async def getbyte(self, url: str) -> BytesIO:
        """
        Get the BytesIO object of an url
        """

        return BytesIO(await self.session.get_bytes(url))

    async def create_db(self) -> asyncpg.Pool:
        """
        Create a connection to the postgresql database
        """

        log.info("Creating db connection")
        return await asyncpg.create_pool(**self.login_data)


    async def get_context(
        self, message: discord.Message, cls=PretendContext
    ) -> PretendContext:
        """
        Get the bot's custom context
        """

        return await super().get_context(message, cls=cls)

    async def autoposting(self, kind: str):
        if getattr(self, f"{kind}_send"):
            results = await self.db.fetch("SELECT * FROM autopfp WHERE type = $1", kind)

            while results:
                for result in results:
                    if channel := self.get_channel(result.channel_id):
                        await asyncio.sleep(0.001)
                        directory = f"cogs/api/PretendImages/{kind.capitalize()}"
                        category = (
                            result.category
                            if result.category != "random"
                            else random.choice(os.listdir(directory))
                        ).capitalize()
                        if category in os.listdir(directory):
                            try:
                                directory += f"/{category}"
                                file_path = (
                                    directory
                                    + "/"
                                    + random.choice(os.listdir(directory))
                                )
                                file = discord.File(file_path)
                                embed = (
                                    discord.Embed(color=self.color)
                                    .set_image(url=f"attachment://{file.filename}")
                                    .set_footer(
                                        text=f"{result.type} module: {category} • id: {file.filename[:-4]}"
                                    )
                                )

                                await channel.send(embed=embed, file=file)
                                await asyncio.sleep(4)
                            except Exception as e:
                                await self.get_channel(1270136983473229986).send(
                                    f"{kind} posting error - {e}"
                                )

                results = await self.db.fetch(
                    "SELECT * FROM autopfp WHERE type = $1", kind
                )
                await asyncio.sleep(7)

            channel = self.get_channel(1270136983473229986)
            if not channel:
                return
            await channel.send(f"Stopped sending {kind}")
            setattr(self, f"{kind}_send", False)

    async def start_loops(self) -> None:
        """
        Start all the loops
        """

        shit_loop.start(self)
        snipe_delete.start(self)
        pomelo_task.start(self)
        gw_loop.start(self)
        bump_remind.start(self)
#        check_monthly_guilds.start(self)
        reminder_task.start(self)
        counter_update.start(self)

    def url_encode(self, url: str):
        """
        Encode an url
        """

        return urllib.parse.unquote(urllib.parse.quote_plus(url))

    async def setup_hook(self) -> None:
        from .redis import PretendRedis

        self.redis = await PretendRedis.from_url()


        log.info("Starting bot")
        if not self.db:
            self.db = await self.create_db()

        self.bot_invite = discord.utils.oauth_url(
            client_id=self.user.id, permissions=discord.Permissions(8)
        )
        await self.load()

    async def load(self) -> None:
        """
        load all cogs
        """

        await self.load_extension("jishaku")
        log.info("Loaded jishaku")

        for file in [f[:-3] for f in os.listdir("./cogs") if f.endswith(".py")]:
            try:
                await self.load_extension(f"cogs.{file}")
            except:
                log.error(f"Unable to load {file}")

        for file in [f[:-3] for f in os.listdir("./events") if f.endswith(".py")]:
            await self.load_extension(f"events.{file}")

        log.info("Loaded all cogs")
        await self.load_views()
        log.info("Loaded views")

    async def load_views(self) -> None:
        """
        Add the persistent views
        """

        logging_view = LogsView()
        logging_view.add_item(UserBan())
        self.add_view(logging_view)
        vm_results = await self.db.fetch("SELECT * FROM vm_buttons")
        self.add_view(VoiceMasterView(self, vm_results))
        self.add_view(GiveawayView())
        self.add_view(TicketView(self, True))

    async def __chunk_guilds(self):
        for guild in self.guilds:
            await asyncio.sleep(2)
            await guild.chunk(cache=True)

    async def on_ready(self) -> None:
        log.info(f"Connected as {self.user}")
        asyncio.ensure_future(self.__chunk_guilds())
        await Music(self).start_nodes()
#        asyncio.ensure_future(self.autoposting("pfps"))
#        asyncio.ensure_future(self.autoposting("banners"))
        await self.start_loops()

    async def on_command_error(
        self, ctx: PretendContext, error: commands.CommandError
    ) -> Any:
        """
        The place where the command errors raise
        """
        channel_perms = ctx.channel.permissions_for(ctx.guild.me)

        if not channel_perms.send_messages or not channel_perms.embed_links:
            return

        ignored = [commands.CheckFailure, commands.NotOwner]

        if type(error) in ignored:
            return
        
        if isinstance(error, commands.MemberNotFound):
            return await ctx.send_warning(f"Member not found")
        
        elif isinstance(error, commands.UserNotFound):
            return await ctx.send_warning(f"User not found")
        
        elif isinstance(error, commands.ThreadNotFound): 
            return await ctx.send_warning(f"I was unable to find the thread **{error.argument}**")
        
        elif isinstance(error, commands.EmojiNotFound): 
            return await ctx.send_warning(f"Unable to convert {error.argument} into an **emoji**")
        
        elif isinstance(error, commands.RoleNotFound):
            return await ctx.send_warning(f"Role not found")
        
        elif isinstance(error, commands.ChannelNotFound):
            return await ctx.send_warning(f"Channel not found")
        
        elif isinstance(error, commands.GuildNotFound):
            return await ctx.send_warning(f"Guild not found")
        
        elif isinstance(error, commands.UserConverter): 
            return await ctx.send_warning(f"Couldn't convert that into an **user** ")
        
        elif isinstance(error, commands.MemberConverter): 
            return await ctx.send_warning("Couldn't convert that into a **member**")
        
        elif isinstance(error, commands.BotMissingPermissions): 
            return await ctx.send_warning(f"I do not have enough **permissions** to execute this command")

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send_warning(
                f"You are **missing** the following permission: `{', '.join(permission for permission in error.missing_permissions)}`"
            )

        elif isinstance(error, commands.BadUnionArgument):
            if error.converters == (discord.Member, discord.User):
                return await ctx.send_warning(f"Member not found")
            elif error.converters == (discord.Guild, discord.Invite):
                return await ctx.send_warning(f"Invalid invite code")
            else:
                return await ctx.send_warning(
                    f"Couldn't convert **{error.param.name}** into "
                    + f"`{', '.join(converter.__name__ for converter in error.converters)}`"
                )
        elif isinstance(error, commands.BadArgument):
            return await ctx.send_warning(error)
        elif isinstance(error, commands.MissingRequiredArgument):
            if isinstance(ctx.command, commands.Group):
                return await ctx.send_help(ctx.command)
            return await ctx.send_help(ctx.command)

        elif isinstance(error, commands.CommandNotFound):
            if check := await self.db.fetchrow(
                """
        SELECT * FROM aliases
        WHERE guild_id = $1
        AND alias = $2
        """,
                ctx.guild.id,
                ctx.invoked_with,
            ):
                message = copy(ctx.message)
                message.content = message.content.replace(
                    ctx.invoked_with, check["command"]
                )

                return await self.process_commands(message)
            else:
                return
            
        elif isinstance(error, commands.BadInviteArgument): 
            return await ctx.send_warning(f"Invalid **invite code** given")
        
        elif isinstance(error, discord.NotFound): 
            return await ctx.send_warning(f"**Not found** - the **ID** is invalid")

        elif isinstance(error, discord.HTTPException):
            if error.code == 50035:
                return await ctx.send_warning(
                    f"Failed to send **embed**\n```{error}```"
                )
        elif isinstance(error, aiohttp.ClientConnectionError):
            return await ctx.send_error(f"Failed to connect to the **API**")
        elif isinstance(error, aiohttp.ClientResponseError):
            if error.status == 522:
                return await ctx.send_warning(
                    f"Timed out while getting data from the **API**"
                )
            else:
                return await ctx.send_warning(
                    f"API returned `{error.status}`, try again later"
                )

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.pretend_send(
                f"Wait **{error.retry_after:.2f} seconds** before using **{ctx.command.qualified_name}** again"
            )

        elif isinstance(
            error, commands.CommandRegistrationError
        ):  # this should never be used anywhere besides ValidCog
            return await ctx.send(error)

        elif isinstance(
            error, commands.CommandError
        ) and not "Command raised an exception: " in str(error):
            return await ctx.send_warning(error)

        else:
            print(str(error))
            code = "".join(
                random.choice(string.ascii_letters + string.digits) for _ in range(6)
            )
            now = discord.utils.format_dt(datetime.datetime.now(), style="R")

            j = {
                "guild_id": ctx.guild.id,
                "channel_id": ctx.channel.id,
                "user_id": ctx.author.id,
                "timestamp": now,
                "error": str(error),
                "code": code,
                "command": str(ctx.command.qualified_name) or "N/A",
            }

            await self.db.execute(
                """
        INSERT INTO error_codes (code, info)
        VALUES ($1, $2)
        """,
                code,
                json.dumps(j),
            )
            embed = discord.Embed(
                description=f"{self.warning} {ctx.author.mention}: An error occurred while running the **{ctx.command.qualified_name}** command."
                + f"\nPlease report the attached code to a developer in the [pretend server](https://discord.gg/7jUMQ6YnX5)",
                color=self.w_color,
            )

            return await ctx.send(embed=embed, content=f"`{code}`")

    def dt_convert(self, datetime: datetime.datetime) -> str:
        """
        Get a detailed version of a datetime value
        """

        hour = datetime.hour

        if hour > 12:
            meridian = "PM"
            hour -= 12
        else:
            meridian = "AM"

        return f"{datetime.month}/{datetime.day}/{str(datetime.year)[-2:]} at {hour}:{datetime.minute} {meridian}"

    async def get_prefixes(self, message: discord.Message) -> Set[str]:
        """
        Returns a list of the bot's prefixes
        """

        prefixes = set()
        r = await self.db.fetchrow(
            "SELECT prefix FROM selfprefix WHERE user_id = $1", message.author.id
        )
        if r:
            prefixes.add(r[0])
        re = await self.db.fetchrow(
            "SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id
        )
        if re:
            prefixes.add(re[0])
        else:
            prefixes.add(";")
        return set(prefixes)

    def member_cooldown(self, message: discord.Message) -> Optional[int]:
        bucket = self.mcd.get_bucket(message)
        return bucket.update_rate_limit()

    def channel_cooldown(self, message: discord.Message) -> Optional[int]:
        bucket = self.ccd.get_bucket(message)
        return bucket.update_rate_limit()

    def is_dangerous(self, role: discord.Role) -> bool:
        """
        Check if the role has dangerous permissions
        """

        return any(
            [
                role.permissions.ban_members,
                role.permissions.kick_members,
                role.permissions.mention_everyone,
                role.permissions.manage_channels,
                role.permissions.manage_events,
                role.permissions.manage_expressions,
                role.permissions.manage_guild,
                role.permissions.manage_roles,
                role.permissions.manage_messages,
                role.permissions.manage_webhooks,
                role.permissions.manage_permissions,
                role.permissions.manage_threads,
                role.permissions.moderate_members,
                role.permissions.mute_members,
                role.permissions.deafen_members,
                role.permissions.move_members,
                role.permissions.administrator,
            ]
        )

    async def process_commands(self, message: discord.Message) -> Any:
        """
        Process a command from the given message
        """

        if message.content.startswith(
            tuple(await self.get_prefixes(message))
        ) or message.content.startswith(f"<@{self.user.id}>"):
            channel_rl = self.channel_cooldown(message)
            member_rl = self.member_cooldown(message)

            if channel_rl or member_rl:
                return

            return await super().process_commands(message)

    async def on_message_edit(
        self, before: discord.Message, after: discord.Message
    ) -> Any:
        if not after.guild:
            return

        if before.content != after.content:

            if after.content.startswith(
                tuple(await self.get_prefixes(after))
            ) or after.content.startswith(f"<@{self.user.id}>"):
                return await self.process_commands(after)

    async def check_availability(
        self, message: discord.Message, ctx: PretendContext
    ) -> bool:
        return True

    async def on_message(self, message: discord.Message) -> Any:
        if not message.author.bot and message.guild:
            perms = message.channel.permissions_for(message.guild.me)
            if perms.send_messages and perms.embed_links:
                if not await self.db.fetchrow(
                    "SELECT * FROM blacklist WHERE id = $1 AND type = $2",
                    message.author.id,
                    "user",
                ):
                    if message.content == f"<@{self.user.id}>":
                        channel_rl = self.channel_cooldown(message)
                        member_rl = self.member_cooldown(message)

                        if not channel_rl and not member_rl:
                            ctx = await self.get_context(message)
                            if await self.check_availability(message, ctx):
                                prefixes = ", ".join(
                                    f"`{p}`" for p in await self.get_prefixes(message)
                                )
                                return await ctx.send(
                                    embed=discord.Embed(
                                        color=self.color,
                                        description=f"{'prefix is' if len(await self.get_prefixes(message)) == 1 else 'prefixes'}: {prefixes}",
                                    )
                                )

                    await self.process_commands(message)


async def getprefix(bot: Pretend, message: discord.Message) -> List[str]:
    """
    Return the actual prefixes for the bot
    """

    if message.guild:
        prefixes = list(map(lambda x: x, await bot.get_prefixes(message)))
        return commands.when_mentioned_or(*prefixes)(bot, message)
