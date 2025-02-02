
from tools.bot import Pretend
from tools.helpers import PretendContext

from discord import User, Embed, __version__, utils, Permissions
from discord.ext.commands import Cog, command, hybrid_command
from discord.ui import View, Button

from platform import python_version


class Info(Cog):
    def __init__(self, bot: Pretend):
        self.bot = bot
        self.description = "Information commands"

    def create_bot_invite(self, user: User) -> View:
        """
        Create a view containing a button with the bot invite url
        """

        view = View()
        view.add_item(
            Button(
                label=f"invite {user.name}",
                url=utils.oauth_url(client_id=user.id, permissions=Permissions(8)),
            )
        )
        return view

    @hybrid_command(name="commands", aliases=["h", "cmds"])
    async def _help(self, ctx: PretendContext, *, command: str = None):
        """
        The help command menu
        """

        if not command:
            return await ctx.send_help()
        else:
            _command = self.bot.get_command(command)
            if (
                _command is None
                or (cog := _command.cog_name)
                and cog.lower() in ["jishaku", "owner", "auth"]
                or _command.hidden
            ):
                return await ctx.send(f'No command called "{command}" found.')

            return await ctx.send_help(_command)

    @command()
    async def getbotinvite(self, ctx: PretendContext, *, member: User):
        """
        Get the bot invite based on it's id
        """

        if not member.bot:
            return await ctx.send_error("This is **not** a bot")

        await ctx.reply(ctx.author.mention, view=self.create_bot_invite(member))

    @hybrid_command()
    async def ping(self, ctx: PretendContext):
        """
        Displays the bot's latency
        """

        await ctx.reply(
            embed=Embed(
                color=self.bot.color,
                description=f"📡 {ctx.author.mention}: ping `{round(self.bot.latency * 1000)}ms`",
            )
        )

    @hybrid_command(aliases=["up"])
    async def uptime(self, ctx: PretendContext):
        """
        Displays how long has the bot been online for
        """

        return await ctx.reply(
            embed=Embed(
                color=self.bot.color,
                description=f"🕰️ {ctx.author.mention}: **{self.bot.uptime}**",
            )
        )

    @hybrid_command(aliases=["bi", "bot", "info", "about"])
    async def botinfo(self, ctx: PretendContext):
        """
        Displays information about the bot
        """

        embed = (
            Embed(
                color=self.bot.color,
                description=f"Multi-purpose Discord bot made by [**Pretend Developers**](https://discord.gg/7jUMQ6YnX5)\nUsed by **{sum(g.member_count for g in self.bot.guilds):,}** members in **{len(self.bot.guilds):,}** servers",
            )
            .set_author(
                name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
            )
            .add_field(
                name="System",
                value=f"**commands:** {len(set(self.bot.walk_commands()))}\n**discord.py:** {__version__}\n**Python:** {python_version()}\n**Lines:** {self.bot.lines:,}",
            )
            .set_footer(text=f"Running for {self.bot.uptime}")
        )
        await ctx.reply(embed=embed)

    @hybrid_command()
    async def shards(self, ctx: PretendContext):
        """
        Check status of each bot shard
        """

        embed = Embed(
            color=self.bot.color, title=f"Total shards ({self.bot.shard_count})"
        )

        for shard in self.bot.shards:
            guilds = [g for g in self.bot.guilds if g.shard_id == shard]
            users = sum([g.member_count for g in guilds])
            embed.add_field(
                name=f"Shard {shard}",
                value=f"**ping**: {round(self.bot.shards.get(shard).latency * 1000)}ms\n**guilds**: {len(guilds)}\n**users**: {users:,}",
                inline=False,
            )

        await ctx.reply(embed=embed)

    @hybrid_command(aliases=["inv", "link"])
    async def invite(self, ctx: PretendContext):
        """
        Send an invite link of the bot
        """

        await ctx.reply(ctx.author.mention, view=self.create_bot_invite(ctx.guild.me))

    @hybrid_command(name="credits")
    async def credits(self, ctx: PretendContext):
        """
        Get more specific credits for the bot
        """

        embed = Embed(
            description=f"[**marian**](https://discord.com/users/852784127447269396): Owns the bot, developer\n[**opex**](https://discord.com/users/1246380245272231987): Developer", color=self.bot.color,
        ).set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)

        await ctx.reply(embed=embed)



#    @command(name="testembeds")
#    async def testembeds(self, ctx: PretendContext):
#        await ctx.send_warning("This is a warning message.")
#        await ctx.send_error("This is an error message.")
#        await ctx.send_success("This is a success message.")
#        await ctx.pretend_send("This is a regular pretend message.")
#        await ctx.lastfm_send("This is a Last.fm type message.")
#        await ctx.economy_send("This is an economy message.")
#
#


async def setup(bot: Pretend) -> None:
    return await bot.add_cog(Info(bot))
