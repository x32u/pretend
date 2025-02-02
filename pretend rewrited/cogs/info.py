import discord, datetime
from discord.ext import commands
from discord.ext.commands import Author, Cog, command, has_permissions, hybrid_command
from discord.ui import View, Button
from discord import (
    app_commands
)
from discord import Embed, File, TextChannel, Member, User, Role 
class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.hybrid_command(aliases=["si"])
    async def serverinfo(self, ctx, invite: discord.Invite = None):
        if invite:
            embed = discord.Embed(
                color=self.bot.color, title=f"{invite.code}"
            ).add_field(
                name="Invite",
                value=f">>> **Channel:** {invite.channel.name}\n**Id:** {invite.channel.id}\n**Expires:** {f'yes ({self.bot.humanize_date(invite.expires_at.replace(tzinfo=None))})' if invite.expires_at else 'no'}\n**Uses:** {invite.uses or 'unknown'}",
            )

            if invite.guild:
                embed.description = invite.guild.description or ""
                embed.set_thumbnail(url=invite.guild.icon).add_field(
                    name="Server",
                    value=f">>> **Name:** {invite.guild.name}\n**Id:** {invite.guild.id}\n**Members:** {invite.approximate_member_count:,}\n**Created**: {discord.utils.format_dt(invite.created_at, style='R') if invite.created_at else 'N/A'}",
                )

        else:
            servers = sorted(
                self.bot.guilds, key=lambda g: g.member_count, reverse=True
            )
            embed = (
                discord.Embed(
                    color=self.bot.color,
                    title=ctx.guild.name,
                    description=f"{ctx.guild.description or ''}\n\nCreated on {discord.utils.format_dt(ctx.guild.created_at, style='D')} {discord.utils.format_dt(ctx.guild.created_at, style='R')}\nJoined on {discord.utils.format_dt(ctx.guild.me.joined_at, style='D')} {discord.utils.format_dt(ctx.guild.me.joined_at, style='R')}",
                )
                .set_thumbnail(url=ctx.guild.icon)
                .add_field(
                    name="Counts",
                    value=f"**Roles:** {len(ctx.guild.roles):,}\n**Emojis:** {len(ctx.guild.emojis):,}\n**Stickers:** {len(ctx.guild.stickers):,}",
                )
                .add_field(
                    name="Members",
                    value=f"**Users:** {len(set(i for i in ctx.guild.members if not i.bot)):,}\n**Bots:** {len(set(i for i in ctx.guild.members if i.bot)):,}\n**Total:** {ctx.guild.member_count:,}",
                )
                .add_field(
                    name="Channels",
                    value=f"**Text:** {len(ctx.guild.text_channels):,}\n**Voice:** {len(ctx.guild.voice_channels):,}\n**Categories:** {len(ctx.guild.categories):,}",
                )
                .add_field(
                    name="Info",
                    value=f"**Vanity:** {ctx.guild.vanity_url_code or 'N/A'}\n**Popularity:** {servers.index(ctx.guild)+1}/{len(self.bot.guilds)}",
                )
            )
            embed.add_field(
                name="Boost",
                value=f"**Boosts:** {ctx.guild.premium_subscription_count:,}\n**Level:** {ctx.guild.premium_tier}\n**Boosters:** {len(ctx.guild.premium_subscribers)}",
            ).add_field(
                name="Design",
                value=f"**Icon:** {f'[**here**]({ctx.guild.icon})' if ctx.guild.icon else 'N/A'}\n**Banner:**  {f'[**here**]({ctx.guild.banner})' if ctx.guild.banner else 'N/A'}\n**Splash:**  {f'[**here**]({ctx.guild.splash})' if ctx.guild.splash else 'N/A'}",
            ).set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url=ctx.author.display_avatar.url
            )

        await ctx.send(embed=embed)

    @hybrid_command(aliases=["mc"], description="See how many members the server has")
    async def membercount(self, ctx):
        embed = discord.Embed(color=self.bot.color, description=f"{ctx.guild.member_count} - **members**")
        await ctx.reply(embed=embed)

    @hybrid_command(description="see bot information", aliases=["bi"])
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def botinfo(self, ctx):
        avatar_url = self.bot.user.avatar.url if self.bot.user.avatar else None
        
        embed = discord.Embed(color=self.bot.color, description="").add_field(
            name='Analystics', 
            value=f">>> Ping: **{round(self.bot.latency * 1000)}ms**\nCommands: **{len(self.bot.commands)}**\nShard(s): **{self.bot.shard_count}**", 
            inline=True
        ).add_field(
            name='Information', 
            value=f">>> Servers: **{len(self.bot.guilds)}**\nUsers: **{sum(g.member_count for g in self.bot.guilds):,}**\nDiscord: **{discord.__version__}**", 
            inline=True)
        
        await ctx.reply(embed=embed)

    @hybrid_command(description="see the ping of the bot", aliases=["pong"])
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ping(self, ctx):
        await ctx.send(f"**{round(self.bot.latency * 1000)}ms...**")

    @hybrid_command(description="send the user/your pfp", aliases=["av"])
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def avatar(self, ctx, user: discord.User = None):
        user = user or ctx.author  
        avatar_url = user.display_avatar.url
        embed = discord.Embed(title=f"{user.name}'s Avatar", color=self.bot.color)
        embed.set_image(url=avatar_url)
        await ctx.send(embed=embed)

    @hybrid_command(description="send the user/your banner", aliases=["bnr"])
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def banner(self, ctx, user: discord.User = None):
        user = user or ctx.author  
        
        user = await self.bot.fetch_user(user.id)
        
        if user.banner:
            banner_url = user.banner.url
            embed = discord.Embed(title=f"{user.name}'s Banner", color=self.bot.color)
            embed.set_image(url=banner_url)
        else:
            embed = discord.Embed(description="This user does not have a banner.", color=self.bot.color)
        
        await ctx.send(embed=embed)
    @hybrid_command(description="invite the bot", help="info", aliases=["support", "inv"])
    async def invite(self, ctx):
     embed = discord.Embed(color=self.bot.color, description="Invite **Pretend** in your server !")
     button1 = Button(label="Invite", url=f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands")
     button2 = Button(label="Support", url="https://discord.gg/blonde")
     view = View()
     view.add_item(button1)
     view.add_item(button2)
     await ctx.reply(embed=embed, view=view)

    @hybrid_command(aliases=["firstmsg"], description="get the first message", usage="<channel>")
    async def firstmessage(self, ctx, *, channel: TextChannel=None):
     channel = channel or ctx.channel 
     messages = [mes async for mes in channel.history(oldest_first=True, limit=1)]
     message = messages[0]
     embed = Embed(color=self.bot.color, title="First message in #{}".format(channel.name), description=message.content, timestamp=message.created_at)
     embed.set_author(name=message.author, icon_url=message.author.display_avatar)
     view = View()
     view.add_item(Button(label="Jump To Message", url=message.jump_url))
     await ctx.reply(embed=embed, view=view) 

    @hybrid_command(name="inviteinfo", aliases=["ii"], description="Get information about an invite", usage="<code>")
    async def inviteinfo(self, ctx, code: str):
        if "/" in code:
            code = code.split("/", -1)[-1].replace(" ", "")

        try:
            invite = await ctx.bot.fetch_invite(url=code, with_counts=True, with_expiration=True)
        except discord.NotFound:
            return await ctx.send_warning('That was an invalid invite')
        icon= f"[icon]({invite.guild.icon.url})" if invite.guild.icon is not None else "N/A"
        splash=f"[splash]({invite.guild.splash.url})" if invite.guild.splash is not None else "N/A"
        banner=f"[banner]({invite.guild.banner.url})" if invite.guild.banner is not None else "N/A"
        members_total = f"{invite.approximate_member_count:,}"
        members_online_total = f"{invite.approximate_presence_count:,}"
        ratio_string = round(invite.approximate_presence_count / invite.approximate_member_count, 2) * 100
        urls = ""
        embed = discord.Embed(color=self.bot.color, title=f"Invite Code: {code}")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.add_field(name="Channel & Invite", value=f">>> **Name:** {invite.channel} (**{invite.channel.type}**)\n**ID:** **{invite.channel.id}**\n**Created:** <t:{str(invite.channel.created_at.timestamp()).split('.')[0]}> (<t:{str(invite.channel.created_at.timestamp()).split('.')[0]}:R>)\n**Invite Expiration:** {invite.max_age}\n**Inviter:** {invite.inviter}\n**Temporary:** {invite.temporary}\n**Usage:** {invite.uses}")
        embed.add_field(name="Guild", value=f">>> **Name:** {invite.guild.name}\n**ID:** `{invite.guild.id}`\n**Created:** <t:{str(invite.guild.created_at.timestamp()).split('.')[0]}> (<t:{str(invite.guild.created_at.timestamp()).split('.')[0]}:R>)\n**Members:** {members_total}\n**Members Online:** {members_online_total}\n**Verification Level:** {str(invite.guild.verification_level).title()}")
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)

        if invite.guild.icon is not None:
          embed.set_thumbnail(url=invite.guild.icon.url)

        await ctx.reply(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))