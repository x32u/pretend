import discord
from discord.ext import tasks, commands
import random
import aiohttp

# Replace these imports with your actual imports
from tools.helpers import PretendContext
from tools.bot import Pretend
from tools.predicates import is_autonsfw

# List of endpoints for NSFW content
ends = [ 
    "https://api.night-api.com/images/nsfw/ass", 
    "https://api.night-api.com/images/nsfw/boobs", 
    "https://api.night-api.com/images/nsfw/anal", 
    "https://api.night-api.com/images/nsfw/hentai", 
    "https://api.night-api.com/images/nsfw/hass", 
    "https://api.night-api.com/images/nsfw/pgif",
    "https://api.night-api.com/images/nsfw/gonewild",
    "https://api.night-api.com/images/nsfw/hboobs",
    "https://api.night-api.com/images/nsfw/hanal"
]

class AutoNSFW(commands.Cog):
    def __init__(self, bot: Pretend):
        self.bot = bot
        self.night_api_key = "SHUGpdGbjo-E4Tn9SHjAlJM5HRYj7no-29xXGgss5v"
        self.post_nsfw.start()  # Start the loop

    def cog_unload(self):
        self.post_nsfw.cancel()  # Ensure the loop is canceled when the cog is unloaded

    @tasks.loop(seconds=6)
    async def post_nsfw(self):
        async with self.bot.db.acquire() as connection:  # Use acquire to handle connection lifecycle
            rows = await connection.fetch("SELECT guild_id, channel_id FROM autonsfw")
            for row in rows:
                guild = self.bot.get_guild(row['guild_id'])
                if guild:
                    channel = guild.get_channel(row['channel_id'])
                    if channel:
                        await self.fetch_and_post_image(channel)

    async def fetch_and_post_image(self, channel: discord.TextChannel):
        endpoint = random.choice(ends)
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.night_api_key,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get("content", {}).get("url")
                    if image_url:
                        embed = discord.Embed(color=self.bot.color)
                        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)
                        embed.set_image(url=image_url)
                        await channel.send(embed=embed)
    """                    
    @commands.Cog.listener()
    async def on_ready(self):
        async with self.bot.db.acquire() as connection:
            await connection.execute("CREATE TABLE IF NOT EXISTS nsfw_toggle (guild_id BIGINT, status BOOLEAN)")
            await connection.execute("CREATE TABLE IF NOT EXISTS autonsfw (guild_id BIGINT, channel_id BIGINT)")
    """
                   
    @commands.group(name="autonsfw", invoke_without_command=True)
    async def autonsfw(self, ctx: PretendContext):
        return await ctx.create_pages()

    @autonsfw.command(name="toggle", brief="Toggle auto-NSFW feature")
    @commands.has_guild_permissions(manage_channels=True)
    async def auto_toggle(self, ctx: PretendContext):
        async with self.bot.db.acquire() as connection:
            result = await connection.fetchrow("SELECT * FROM nsfw_toggle WHERE guild_id = $1", ctx.guild.id)
            if result:
                new_status = not result['status']
                await connection.execute("UPDATE nsfw_toggle SET status = $1 WHERE guild_id = $2", new_status, ctx.guild.id)
            else:
                new_status = True
                await connection.execute("INSERT INTO nsfw_toggle (guild_id, status) VALUES ($1, $2)", ctx.guild.id, new_status)
            await ctx.send_success(f"Auto-NSFW is now {'enabled' if new_status else 'disabled'}.")

    @autonsfw.command(name="start")
    @commands.has_guild_permissions(manage_channels=True)
    @is_autonsfw()
    async def start(self, ctx: PretendContext, channel: discord.TextChannel = None):
        if not channel:
            await ctx.send_warning("Please provide a channel.")
            return

        if not channel.is_nsfw():
            await ctx.send_warning("The provided channel is not marked as NSFW.")
            return

        async with self.bot.db.acquire() as connection:
            result = await connection.fetchrow("SELECT * FROM autonsfw WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
            if result:
                await ctx.send_warning("Auto-NSFW is already enabled in this channel.")
            else:
                await connection.execute("INSERT INTO autonsfw (guild_id, channel_id) VALUES ($1, $2)", ctx.guild.id, channel.id)
                await ctx.send_success(f"Auto-NSFW started in {channel.mention}.")

    @autonsfw.command(name="stop")
    @commands.has_guild_permissions(manage_channels=True)
    @is_autonsfw()
    async def stop(self, ctx: PretendContext, channel: discord.TextChannel = None):
        if not channel:
            await ctx.send_warning("Please provide a channel.")
            return

        async with self.bot.db.acquire() as connection:
            result = await connection.fetchrow("SELECT * FROM autonsfw WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
            if not result:
                await ctx.send_error("Auto-NSFW is not enabled in this channel.")
            else:
                await connection.execute("DELETE FROM autonsfw WHERE guild_id = $1 AND channel_id = $2", ctx.guild.id, channel.id)
                await ctx.send_success(f"Auto-NSFW stopped in {channel.mention}.")

    @autonsfw.command(name="list")
    @commands.has_guild_permissions(manage_channels=True)
    @is_autonsfw()
    async def list_channels(self, ctx: PretendContext):
        async with self.bot.db.acquire() as connection:
            results = await connection.fetch("SELECT channel_id FROM autonsfw WHERE guild_id = $1", ctx.guild.id)
            if not results:
                await ctx.send_warning("No channels found with Auto-NSFW enabled.")
                return

            channels = [ctx.guild.get_channel(record['channel_id']) for record in results]
            channels = [channel for channel in channels if channel is not None]

            if not channels:
                await ctx.send_warning("No channels found with Auto-NSFW enabled.")
                return

            embed = discord.Embed(color=self.bot.color)
            embed.description = "\n".join(f"{i + 1}. {channel.mention}" for i, channel in enumerate(channels))
            await ctx.send(embed=embed)

async def setup(bot: Pretend):
    await bot.add_cog(AutoNSFW(bot))
