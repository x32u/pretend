import sys
import discord
from discord.ext import commands
from pretend.config import token, color, yes, no, warning
from pretend.context import getprefix, HelpCommand, context, ping
from asyncpg import create_pool
import os

intents = discord.Intents.all()
intents.presences = False

class Pretend(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=getprefix,
            intents=intents,
            help_command=HelpCommand(),
            chunk_guilds_at_startup=False,
            owner_ids=[
                852784127447269396,
                713128996287807600
            ],
            case_insensitive=True,
            strip_after_prefix=True,
            enable_debug_events=True,
            activity=discord.Activity(name="rewrite gg/blonde", type=discord.ActivityType.competing),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, roles=False, replied_user=False
            ),
        )
        self.color = color
        self.yes = yes
        self.no = no
        self.warning = warning
        self.ping = ping

    async def get_context(self, message, *, cls=context):
        return await super().get_context(message, cls=cls) 

    async def create_db_pool(self):
        self.db = await create_pool(
            port="5432",
            database="postgres",
            user="postgres.pexxcoqyhdudkxrzxidm",
            host="aws-0-us-east-1.pooler.supabase.com",
            password="9LLlJMUCUIvQ5ebp"
        )

    async def setup_hook(self):
        await self.create_db_pool()
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                await self.load_extension("cogs." + file[:-3])
                print(f'{file[:-3]} = LOADED')
        await self.load_extension("jishaku")

bot = Pretend()
bot.run(token)
