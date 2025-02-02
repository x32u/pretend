import discord, psutil, datetime
from datetime import timedelta, datetime
import os
from discord.ext import commands
from get.pretend import Pretend
from get.pretend import PretendContext
from discord import User, Embed, __version__, utils, Permissions
from discord.ext.commands import Cog, command, hybrid_command
from discord.ui import View, Button
from platform import python_version
import humanize
from get.time import humanize, human_timedelta
from psutil._common import bytes2human as natural_size

class Info(commands.Cog):
    def __init__(self, bot: Pretend):
        self.bot = bot

    @command(
        name="bggggggotinfo",
        aliases=[
            'abgggout',
            'ggggbi'
        ]
    )
    async def botingggfo(
        self,
        ctx: PretendContext
    ):
        """
        Get info on bot
        """

        summary = [
            f"Bot created and maintained by marian\n"
            f"> Bot using dpy {discord.__version__}\n"
            ""
        ]

        if psutil:
            try:
                proc = psutil.Process()

                with proc.oneshot():
                    try:
                        mem = proc.memory_full_info()
                        summary.append(f"Using `{natural_size(mem.rss)} physical memory` and "
                                       f"`{natural_size(mem.vms)} virtual memory`, "
                                       f"`{natural_size(mem.uss)}` of which unique to this process.")
                    except psutil.AccessDenied:
                        pass

                    try:

                        summary.append(f"Utilizing `{len(self.bot.commands)} command(s)`.")
                    except psutil.AccessDenied:
                        pass

                    summary.append("")  # blank line
            except psutil.AccessDenied:
                summary.append(
                    "psutil is installed, but this process does not have high enough access rights "
                    "to query process information."
                )
                summary.append("")  # blank line

        cache_summary = f"`{len(self.bot.guilds):,} guild(s)` and `{len(self.bot.users):,} user(s)`"

        shard_ids = ', '.join(str(i) for i in self.bot.shards.keys())
        summary.append(
            f"This bot is sharded (Shards {shard_ids} of {self.bot.shard_count})"
            f" and can see {cache_summary}."
        )

        summary.append(f"**Average websocket latency: {round(self.bot.latency * 1000, 2)}ms**")

        e = Embed(
            description="\n".join(summary)
        ).set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=e)

    @hybrid_command(aliases=["bi", "bot", "info", "about"])
    async def botinfo(self, ctx: PretendContext):
        cpu_usage = psutil.cpu_percent()
        disk_usage = psutil.disk_usage('/').percent
        net_io_counters = psutil.net_io_counters()
        bandwidth_usage = (net_io_counters.bytes_sent + net_io_counters.bytes_recv) / 1024 / 1024
        embed = (
            Embed(
                color=self.bot.color,
                description=f"Multi-purpose discord bot made by [**Pretend Team**](https://discord.com/invite/pretendbot)\nUsed by **{sum(g.member_count for g in self.bot.guilds):,}** members in **{len(self.bot.guilds):,}** servers",
            )
            .set_author(
                name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
            )
            .add_field(
                name="System",
                value=f"**Commands:** {len(set(self.bot.walk_commands()))}\n**Lines:** {self.bot.lines:,}\n**Ping:** {self.bot.latency*1000:.2f}ms\n**Disk:** {disk_usage}%\n**Bandwidth:** {bandwidth_usage:.2f}\n**CPU:** {cpu_usage}%",
            )
        )
        await ctx.send(embed=embed)


    @command(help="info", description="get bot invite", aliases=["inv", "link"])
    async def invite(self, ctx):
        """
        Send an invite link of the bot
        """

        await ctx.reply("pretend click [here](https://discordapp.com/oauth2/authorize?client_id=1263734958586073141&scope=bot+applications.commands&permissions=8)")

    @command()
    async def ping(self, ctx):
        e = discord.Embed(
            color=self.bot.color,
            description=f"📡 **{round(self.bot.latency * 1000)}ms**")
        await ctx.reply(embed=e, mention_author=False)

    @command(description="get a user with nitro boost, icon and banner", help="info", aliases=["pi"])
    async def profileicon(self, ctx, *, member: discord.User = None):
        if member == None:member = ctx.author
        user = await self.bot.fetch_user(member.id)
        if user.banner == None:
            em = discord.Embed(
                color=self.bot.color,
                description=f"{member.mention}: doesn't have a profile banner I can display.")
            await ctx.reply(embed=em, mention_author=False)
        else:
            banner_url = user.banner.url
            avatar_url = user.avatar.url
            button1 = Button(label="Icon", url=avatar_url)
            button2 = Button(label="Banner", url=banner_url)
            e = discord.Embed(color=self.bot.color, description=f'*Here is the icon and banner for [**{member.display_name}**](https://discord.com/users/{member.id})*')
            e.set_author(name=f"{member.display_name}", icon_url=f"{member.avatar}", url=f"https://discord.com/users/{member.id}")
            e.set_image(url=f"{banner_url}")
            e.set_thumbnail(url=f"{avatar_url}")
            view = View()
            view.add_item(button1)
            view.add_item(button2)
            await ctx.reply(embed=e, view=view, mention_author=False)

    @command(help="info", description="get bot status", name='status')
    async def status(self, ctx):
        """Displays bot statistics."""
        # Calculate uptime

        # Calculate bot ping
        latency = round(self.bot.latency * 1000)

        # Get bot process memory usage
        process = psutil.Process()
        memory_usage = process.memory_full_info().rss / 1024 ** 2

        # Get shard information
        shard_id = ctx.guild.shard_id if ctx.guild else 0
        shard_count = self.bot.shard_count

        # Send statistics embed
        embed = discord.Embed(title="pretend info xd", color=self.bot.color)
        embed.add_field(name="Ping", value=f"{latency}ms", inline=False)
        embed.add_field(name="Memory Usage", value=f"{memory_usage:.2f} MB", inline=False)
        embed.add_field(name="Shard ID", value=str(shard_id), inline=True)
        embed.add_field(name="Shard Count", value=str(shard_count), inline=True)
        await ctx.send(embed=embed)
    @hybrid_command(name="credits")
    async def credits(self, ctx: PretendContext):
        """
        Get more specific credits for the bot
        """

        embed = Embed(
            description=f"[**Marian**](<https://discord.com/users/852784127447269396>): bot developer"
            + f"\n[**Waiser**](<https://discord.com/users/1188163689208090684>): web developer + developer"
            + f"\n[**Karlo**](<https://discord.com/users/1015714172195049502>): hosting provider",
            color=self.bot.color,
        ).set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)

        await ctx.send(embed=embed)
async def setup(bot: Pretend) -> None:
    return await bot.add_cog(Info(bot))