import discord
import datetime

from discord.ext import commands

from typing import Union

from tools.helpers import PretendContext
from tools.predicates import auth_perms


class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1320013224661356664

    async def guild_change(self, state: str, guild: discord.Guild):
        await self.bot.get_channel(self.channel_id).send(
            embed=discord.Embed(
                description=f"{state} **{guild.name}** (`{guild.id})`",
                color=self.bot.color,
            )
            .add_field(name="owner", value=guild.owner)
            .add_field(name="member count", value=guild.member_count)
        )

    async def add_subscriber(self, user: discord.User):
        """
        add the subscriber role to the subscriber
        """

        if member := self.bot.get_guild(1177424668328726548).get_member(user.id):
            if role := member.guild.get_role(1183427233801584723):
                await member.add_roles(role, reason="A new subscriber")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        if not self.bot.is_ready():
            return

        await self.guild_change("left", guild)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if not guild.chunked:
            await guild.chunk(cache=True)

        await self.guild_change("joined", guild)

    @commands.group(invoke_without_command=True)
    @auth_perms()
    async def auth(self, ctx):
        """
        Auth group command
        """

        await ctx.create_pages()

    @auth.group(invoke_without_command=True, name="add")
    @auth_perms()
    async def auth_add(self, ctx: PretendContext):
        """
        Authorize a server
        """

        await ctx.create_pages()

    @auth_add.command(name="onetime")
    @auth_perms()
    async def auth_add_onetime(
        self,
        ctx: PretendContext,
        user: discord.User,
        invite: Union[discord.Invite, int],
    ):
        """
        Authorize a server (onetime subscription)
        """

        if isinstance(invite, discord.Invite):
            invite = invite.guild.id

        if await self.bot.db.fetchrow(
            "SELECT * FROM authorize WHERE guild_id = $1", invite
        ):
            return await ctx.reply("This guild is **already** authorized")

        await self.bot.db.execute(
            """
      INSERT INTO authorize
      VALUES ($1,$2,$3,$4)
      """,
            invite,
            user.id,
            None,
            2,
        )

        await self.add_subscriber(user)
        channel = self.bot.get_channel(1183429412406951966)

        embed = (
            discord.Embed(color=self.bot.color, title="onetime subscription added")
            .set_author(
                name=str(ctx.author),
                icon_url=ctx.author.display_avatar.url,
            )
            .add_field(name="type", value="onetime")
            .add_field(name="price", value="$10")
            .add_field(name="buyer", value=str(user))
            .set_footer(text=f"guild id: {invite}")
        )

        await channel.send(embed=embed)
        return await ctx.pretend_send(
            f"Authorized **{invite}**, requested by **{user}** (onetime)"
        )

    @auth_add.command(name="monthly")
    @auth_perms()
    async def auth_add_monthly(
        self,
        ctx: PretendContext,
        user: discord.User,
        invite: Union[discord.Invite, int],
    ):
        """
        Authorize a server (monthly subscription)
        """

        if isinstance(invite, discord.Invite):
            invite = invite.guild.id

        if await self.bot.db.fetchrow(
            "SELECT * FROM authorize WHERE guild_id = $1", invite
        ):
            return await ctx.reply("This guild is **already** authorized")

        next = datetime.datetime.now() + datetime.timedelta(days=30)
        await self.add_subscriber(user)
        await self.bot.db.execute(
            "INSERT INTO authorize VALUES ($1,$2,$3,$4)", invite, user.id, next, 2
        )
        channel = self.bot.get_channel(1183429412406951966)

        embed = (
            discord.Embed(color=self.bot.color, title="monthly subscription added")
            .set_author(
                name=str(ctx.author),
                icon_url=ctx.author.display_avatar.url,
            )
            .add_field(name="type", value="monthly")
            .add_field(name="price", value="$10")
            .add_field(name="buyer", value=str(user))
            .add_field(
                name="billing date", value=f"On {next.day}/{next.month}/{next.year}"
            )
            .set_footer(text=f"guild id: {invite}")
        )

        await channel.send(embed=embed)
        return await ctx.pretend_send(
            f"Authorized **{invite}**, requested by **{user}** (monthly)"
        )

    @auth.command(name="update")
    @auth_perms()
    async def auth_update(
        self, ctx: PretendContext, invite: Union[discord.Invite, int]
    ):
        """
        Update the monthly authorization for a server
        """

        if isinstance(invite, discord.Invite):
            invite = invite.guild.id

        check = await self.bot.db.fetchrow(
            "SELECT * FROM authorize WHERE guild_id = $1 AND till IS NOT NULL", invite
        )

        if not check:
            return await ctx.reply(
                "THis guild is **not** authorized with a monthly offer"
            )

        old_datetime = check["till"]

        await self.bot.db.execute(
            """
    UPDATE authorize
    SET till = $1
    WHERE guild_id = $2
    """,
            (old_datetime + datetime.timedelta(days=30)),
            invite,
        )

        return await ctx.send_success(f"Updated monthly payment for **{invite}**")
    
    @commands.is_owner()
    @commands.command(aliases=["gg"], description="show information about a server", brief="bot owner")
    async def getguild(self, ctx: commands.Context, guild:int):
        guild = self.bot.get_guild(int(guild))   
        if guild == None: 
            return await ctx.warning('no guild found for that id.')
        icon= f"[icon]({guild.icon.url})" if guild.icon is not None else "N/A"
        splash=f"[splash]({guild.splash.url})" if guild.splash is not None else "N/A"
        banner=f"[banner]({guild.banner.url})" if guild.banner is not None else "N/A"   
        desc=guild.description if guild.description is not None else ""
        embed = discord.Embed(color=self.bot.color, title=f"{guild.name}", description=f"{desc}")   
        embed.set_thumbnail(url=guild.icon)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.add_field(name="Owner", value=f"{guild.owner.mention}\n{guild.owner}")
        embed.add_field(name="Members", value=f"**Users:** {len(set(i for i in guild.members if not i.bot))} ({((len(set(i for i in guild.members if not i.bot)))/guild.member_count) * 100:.2f}%)\n**Bots:** {len(set(i for i in guild.members if i.bot))} ({(len(set(i for i in guild.members if i.bot))/guild.member_count) * 100:.2f}%)\n**Total:** {guild.member_count}")
        embed.add_field(name="Information", value=f"**Verification:** {guild.verification_level}\n**Boosts:** {guild.premium_subscription_count} (level {guild.premium_tier})\n**Large:** {'yes' if guild.large else 'no'}")
        embed.add_field(name="Design", value=f"{icon}\n{splash}\n{banner}")
        embed.add_field(name=f"Channels ({len(guild.channels)})", value=f"**Text:** {len(guild.text_channels)}\n**Voice:** {len(guild.voice_channels)}\n**Categories** {len(guild.categories)}")
        embed.add_field(name="Counts", value=f"**Roles:** {len(guild.roles)}/250\n**Emojis:** {len(guild.emojis)}/{guild.emoji_limit*2}\n**Stickers:** {len(guild.stickers)}/{guild.sticker_limit}")
        embed.set_footer(text=f"Guild ID: {guild.id}")
        await ctx.reply(embed=embed)

    @auth.command(name="inspect")
    @auth_perms()
    async def auth_inspect(
        self, ctx: PretendContext, invite: Union[discord.Invite, int]
    ):
        """
        check a guild authorization status
        """

        if isinstance(invite, discord.Invite):
            invite = invite.guild.id

        check = await self.bot.db.fetchrow(
            "SELECT * FROM authorize WHERE guild_id = $1", invite
        )

        if not check:
            return await ctx.reply("This guild id is **not** authorized")

        embed = (
            discord.Embed(
                color=self.bot.color,
                title="Authorization Plan",
                description=f"Subscription type: {'monthly' if check['till'] else 'onetime'}",
            )
            .set_author(name=invite)
            .add_field(name="Buyer", value=f"<@!{check['user_id']}>")
        )

        if check["till"]:
            embed.add_field(
                name="billing date",
                value=self.bot.humanize_date(
                    datetime.datetime.fromtimestamp(check["till"].timestamp())
                ),
            )
        else:
            embed.add_field(name="transfers", value=check["transfers"])

        return await ctx.reply(embed=embed)

    @auth.command(name="getinvite")
    @auth_perms()
    async def auth_getinvite(self, ctx: PretendContext, guild: discord.Guild):
        """
        gets the invite of a authorised server
        """

        try:
            invite = (
                guild.vanity_url
                or (await guild.text_channels[0].create_invite()).url
            )
        except IndexError:
            return await ctx.send_warning(
                "This server doesn't have any available invites"
            )
        except discord.NotFound:
            return await ctx.send_warning(
                "No channels to create an invite were found"
            )

        embed = discord.Embed(
            color=self.bot.color,
            title="Server Invite",
            description=f"The invite for the [server]({invite})",
        )

        return await ctx.reply(embed=embed)

    @auth.command(name="transfer")
    @auth_perms()
    async def auth_transfer(
        self,
        ctx: PretendContext,
        old_inv: Union[discord.Invite, int],
        new_inv: Union[discord.Invite, int],
    ):
        """
        transfer a guild authorization to another guild
        """

        if isinstance(old_inv, discord.Invite):
            old_inv = old_inv.guild.id

        if isinstance(new_inv, discord.Invite):
            new_inv = new_inv.guild.id

        check = await self.bot.db.fetchrow(
            "SELECT * FROM authorize WHERE guild_id = $1", old_inv
        )

        if not check:
            return await ctx.reply("The first guild id is **not** authorized")

        transfers = check["transfers"]
        till = check["till"]
        if transfers == 0:
            return await ctx.send_error("This server has ran out of transfers :(")

        if not till:
            await self.bot.db.execute(
                """
      UPDATE authorize
      SET guild_id = $1, 
      transfers = $2
      WHERE guild_id = $3
      """,
                new_inv,
                transfers - 1,
                old_inv,
            )
        else:
            await self.bot.db.execute(
                """
      UPDATE authorize
      SET guild_id = $1
      WHERE guild_id = $2
      """,
                new_inv,
                old_inv,
            )

        if g := self.bot.get_guild(old_inv):
            await g.leave()

        return await ctx.pretend_send(
            f"Transfered from **{old_inv}** to **{new_inv}**. **{transfers-1}** transfers left!"
        )

    @auth.command(name="remove")
    @auth_perms()
    async def auth_remove(self, ctx: PretendContext, inv: Union[discord.Invite, int]):
        """
        Remove the authorization from a guild
        """

        if isinstance(inv, discord.Invite):
            inv = inv.guild.id

        check = await self.bot.db.fetchrow(
            "SELECT * FROM authorize WHERE guild_id = $1", inv
        )

        if not check:
            return await ctx.reply("This guild is **not** authorized")

        user = check["user_id"]
        await self.bot.db.execute("DELETE FROM authorize WHERE guild_id = $1", inv)
        if guild := self.bot.get_guild(inv):
            await guild.leave()

        val = await self.bot.db.fetchrow(
            "SELECT * FROM authorize WHERE user_id = $1", user
        )
        if not val:
            if support := self.bot.get_guild(1177424668328726548):
                if member := support.get_member(user):
                    if role := support.get_role(1183427233801584723):
                        await member.remove_roles(role)

        return await ctx.pretend_send(f"Unauthorized **{inv}**")

    @auth.command(name="list")
    @auth_perms()
    async def auth_list(self, ctx: PretendContext, *, user: discord.User):
        """
        returns a list of authorized servers by a certain user
        """

        results = await self.bot.db.fetch(
            "SELECT (guild_id) FROM authorize WHERE user_id = $1", user.id
        )

        if not results:
            return await ctx.send_warning(
                "There are no guilds authorized for this member"
            )

        await ctx.paginate(
            [
                f"{f'**{str(self.bot.get_guild(m[0]))}** `{m[0]}`' if self.bot.get_guild(m[0]) else f'`{m[0]}`'}"
                for m in results
            ],
            f"Authorized guilds ({len(results)})",
            {"name": user.name, "icon_url": user.display_avatar.url},
        )


async def setup(bot: commands.AutoShardedBot) -> None:
    await bot.add_cog(Auth(bot))
