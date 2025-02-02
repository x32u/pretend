import uwuify
import asyncio
import discord
import datetime
import humanize
import humanfriendly
import dateutil.parser
import validators
import os
import aiohttp
import json
import requests
from nudenet import NudeDetector

nude_detector = NudeDetector()

from discord.ext.commands import (
   hybrid_command,
   Cog
)
from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException
from discord.ext import commands
from discord.ext.commands import has_guild_permissions
from discord import TextChannel
from playwright.async_api import async_playwright
from io import BytesIO
from typing import Union, Optional, Any
from shazamio import Shazam
from tools.bot import Pretend
from tools.validators import ValidTime
from tools.helpers import PretendContext
from tools.predicates import is_afk, is_there_a_reminder, reminder_exists
from tools.misc.utils import (
    Timezone,
    BdayDate,
    BdayMember,
    TimezoneMember,
    TimezoneLocation,
    get_color,
)

#from tools.handlers.socials.github import GithubUser
#from tools.handlers.socials.snapchat import SnapUser
#from tools.handlers.socials.roblox import RobloxUser
#from tools.handlers.socials.tiktok import TikTokUser
#from tools.handlers.socials.cashapp import CashappUser
#from tools.handlers.socials.instagram import InstagramUser
#from tools.handlers.socials.weather import WeatherLocation
#from deep_translator import GoogleTranslator
#from deep_translator.exceptions import LanguageNotSupportedException
from io import BytesIO

import re
import rembg


class Color(commands.Converter):
    async def convert(self, ctx: PretendContext, argument: str):
        argument = str(argument)

        if argument.lower() in ("random", "rand", "r"):
            return discord.Color.random()
        elif argument.lower() in ("invisible", "invis"):
            return discord.Color.from_str("#2F3136")

        if color := get_color(argument):
            return color
        else:
            raise commands.CommandError(f"Color **{argument}** not found")


class Utility(commands.Cog):
    def __init__(self, bot: Pretend):
        self.bot = bot
        self.tz = Timezone(bot)
        self.description = "Utility commands"
        self.headers = {"Authorization": "3jmzE1vC7mqCTucr"} 
        self.afk_cd = commands.CooldownMapping.from_cooldown(
            3, 3, commands.BucketType.channel
        )

    def human_format(self, number: int) -> str:
        """
        Humanize a number, if the case
        """

        if number > 999:
            return humanize.naturalsize(number, False, True)

        return number.__str__()

    def afk_ratelimit(self, message: discord.Message) -> Optional[int]:
        """
        Cooldown for the afk message event
        """

        bucket = self.afk_cd.get_bucket(message)
        return bucket.update_rate_limit()

    async def cache_profile(self, member: discord.User) -> Any:
        """
        Cache someone's banner
        """

        if member.banner:
            banner = member.banner.url
        else:
            banner = None

        return await self.bot.cache.set(
            f"profile-{member.id}", {"banner": banner}, 3600
        )

    def get_joined_date(self, date) -> str:
        if date.month < 10:
            month = (self.tz.months.get(date.month))[:3]
        else:
            month = (self.tz.months.get(date.month))[:3]

        return f"Joined {month} {date.day} {str(date.year)}"

    @commands.Cog.listener("on_message")
    async def seen_listener(self, message: discord.Message):
        if message.author.bot:
            return

        check = await self.bot.db.fetchrow(
            """
      SELECT * FROM seen
      WHERE user_id = $1
      AND guild_id = $2
      """,
            message.author.id,
            message.guild.id,
        )
        args = [message.author.id, message.guild.id, datetime.datetime.now()]

        if not check:
            await self.bot.db.execute("INSERT INTO seen VALUES ($1,$2,$3)", *args)
        else:
            await self.bot.db.execute(
                "UPDATE seen SET time = $3 WHERE user_id = $1 AND guild_id = $2", *args
            )

    @commands.Cog.listener("on_message")
    async def stickymessage_listener(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        check = await self.bot.db.fetchrow(
            """
      SELECT * FROM stickymessage
      WHERE channel_id = $1
      AND guild_id = $2
      """,
            message.channel.id,
            message.guild.id,
        )
        if check:
            lastmsg = self.bot.cache.get(
                f"sticky-{message.guild.id}-{message.channel.id}"
            )
            if lastmsg:
                lastmsg = await message.channel.fetch_message(str(lastmsg))
                await lastmsg.delete()
            newmsg = await message.channel.send(check["message"])
            await self.bot.cache.set(
                f"sticky-{message.guild.id}-{message.channel.id}", newmsg.id, 3600
            )

    @commands.Cog.listener("on_message")
    async def afk_listener(self, message: discord.Message):
        if message.is_system():
            return

        if not message.guild:
            return

        if not message.author:
            return

        if message.author.bot:
            return

        if check := await self.bot.db.fetchrow(
            "SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2",
            message.guild.id,
            message.author.id,
        ):
            ctx = await self.bot.get_context(message)
            time = check["time"]
            await self.bot.db.execute(
                "DELETE FROM afk WHERE guild_id = $1 AND user_id = $2",
                message.guild.id,
                message.author.id,
            )
            embed = discord.Embed(
                color=self.bot.color,
                description=f"👋 {ctx.author.mention}: Welcome back! You were gone for **{humanize.precisedelta(datetime.datetime.fromtimestamp(time.timestamp()), format='%0.0f')}**",
            )
            return await ctx.reply(embed=embed)

        for mention in message.mentions:
            check = await self.bot.db.fetchrow(
                "SELECT * FROM afk WHERE guild_id = $1 AND user_id = $2",
                message.guild.id,
                mention.id,
            )
            if check:
                if self.afk_ratelimit(message):
                    continue

                ctx = await self.bot.get_context(message)
                time = check["time"]
                embed = discord.Embed(
                    color=self.bot.color,
                    description=f"👋 {ctx.author.mention}: **{mention.name}** is **AFK** for **{humanize.precisedelta(datetime.datetime.fromtimestamp(time.timestamp()), format='%0.0f')}** - {check['reason']}",
                )
                return await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if (before.avatar != after.avatar) or (before.banner != after.banner):
            if before.avatar != after.avatar:
                imgtype = "gif" if before.display_avatar.is_animated() else "png"
                try:

                    async with aiohttp.ClientSession() as session:
                        async with session.request(
                            "POST",
                            "http://127.0.0.1:3030/upload",
                            json={
                                "url": before.display_avatar.url,
                                "type": imgtype,
                                "userid": str(after.id),
                                "name": after.name,
                            },
                            headers={
                                "Authorization": "hmfq0U9odsH3T7X0ICK6oWJN",
                                "Content-Type": "application/json",
                            },
                        ) as r:
                            if r.status != 200:
                                await session.close()
                                return
                            if r.status == 200:
                                await session.close()
                except Exception as e:
                    await session.close()
                    return

            cache = self.bot.cache.get(f"profile-{before.id}")
            if cache:
                await self.cache_profile(after)

    @hybrid_command(description="get a instagram user information", aliases=['ig', 'insta'])
    async def instagram(self, ctx: PretendContext, user: str = None):
        if user is None:
            return await ctx.send_warning("Please provide the username of the Instagram account.")
    
        async with aiohttp.ClientSession(headers=self.headers) as cs:
            async with cs.get("https://api.fulcrum.lol/instagram", params={"username": user}) as r:
                data = await r.json()

            if data.get('detail'):
                return await ctx.send_warning(data['detail'])

            embed = discord.Embed(
                color=self.bot.color, 
                title=data["username"], 
                description=data["bio"]
            )
            embed.add_field(name="Full Name", value=data["full_name"], inline=True)
            embed.add_field(name="Followers", value=data["followers"], inline=True)
            embed.add_field(name="Following", value=data["following"], inline=True)
            embed.add_field(name="ID", value=data["id"], inline=True)
            embed.add_field(name="Posts", value=data["posts"], inline=True)
            embed.add_field(name="Private", value=data["is_private"], inline=True)
            embed.set_thumbnail(url=data["avatar_url"])
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)



    @hybrid_command(description="get a snapchat user information", aliases=['snap'])
    async def snapchat(self, ctx: PretendContext, user: str):
            data = await self.bot.session.get_json(f"https://api.fulcrum.lol/snapchat", headers=self.headers, params={"username": user})
            if data.get('detail'):
              return await ctx.send_warning(data['detail'])

            emb = discord.Embed(
              title=f"{data['display_name']}", 
              description=data["bio"], 
              color=0xffff00
            )
            emb.add_field(name="Username", value=data["username"], inline=True)
            emb.set_image(url=data['snapcode'])
            await ctx.reply(embed=emb)

    @commands.command(aliases=["tr"])
    async def translate(self, ctx: PretendContext, language: str, *, message: str):
        """
        Translate a message to a specific language
        """

        try:
            translator = GoogleTranslator(source="auto", target=language)
            translated = await asyncio.to_thread(translator.translate, message)
            embed = discord.Embed(
                color=self.bot.color,
                title=f"translated to {language}",
                description=f"```{translated}```",
            )

            await ctx.send(embed=embed)
        except LanguageNotSupportedException:
            return await ctx.send_error("This language is **not** supported")

    @commands.command(
        name="roblox",
        description="Shows information on a Roblox user",
        usage=";roblox <username>",
    )
    async def roblox(self, ctx, username):
        try:
            users_json = requests.get(
                f"https://www.roblox.com/search/users/results?keyword={username}&maxRows=1&startIndex=0"
            )
            users = json.loads(users_json.text)

            if "UserSearchResults" not in users or not users["UserSearchResults"]:
                await ctx.send("User not found.")
                return

            user_id = users["UserSearchResults"][0]["UserId"]

            profile_json = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
            profile = json.loads(profile_json.text)

            if (
                "displayName" not in profile
                or "created" not in profile
                or "description" not in profile
            ):
                await ctx.send("An error occurred while fetching user data.")
                return

            display_name = profile["displayName"]
            created_date = profile["created"]
            description = profile["description"]

            avatar_json = requests.get(
                f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=720x720&format=Png&isCircular=false"
            )
            avatar_data = json.loads(avatar_json.text)

            if "data" not in avatar_data or not avatar_data["data"]:
                await ctx.send("An error occurred while fetching user data.")
                return

            avatar_url = avatar_data["data"][0]["imageUrl"]

            followers_json = requests.get(
                f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
            )
            followers_count = json.loads(followers_json.text)["count"]

            embed = discord.Embed(
                title=f"{username}",
                url=f"https://www.roblox.com/users/{user_id}/profile",
                description=f"> **name:** {display_name}\n"
                            f"> **created:** ``{created_date[:10]}``\n"
                            f"> **description:** {description}\n"
                            f"> **followers:** {followers_count}",
                color=self.bot.color
            )
            embed.set_image(url=avatar_url)
            button1 = discord.ui.Button(label="profile", style=discord.ButtonStyle.url, url=f"https://www.roblox.com/users/{user_id}/profile")
            view = discord.ui.View()
            view.add_item(button1)

            await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"An error occurred while fetching user data: {e}")

    @commands.command(aliases=["uwu"])
    async def uwuify(self, ctx: PretendContext, *, message: str):
        """
        Convert a message to the uwu format
        """

        flags = uwuify.YU | uwuify.STUTTER
        embed = discord.Embed(
            color=self.bot.color, description=uwuify.uwu(message, flags=flags)
        )
        return await ctx.reply(embed=embed)

    


    @commands.command(aliases=["firstmsg"])
    async def firstmessage(
        self,
        ctx: PretendContext,
        *,
        channel: discord.TextChannel = commands.CurrentChannel,
    ):
        """
        Get the first message in a channel
        """

        message = [mes async for mes in channel.history(limit=1, oldest_first=True)][0]
        await ctx.pretend_send(
            f"the first message sent in {channel.mention} - [**jump**]({message.jump_url})"
        )

    @commands.hybrid_command(aliases=["av"])
    async def avatar(
        self,
        ctx: PretendContext,
        *,
        member: Union[discord.Member, discord.User] = commands.Author,
    ):
        """
        Return someone's avatar
        """

        embed = discord.Embed(
            color=await self.bot.dominant_color(member.display_avatar.url),
            title=f"{member.name}'s avatar",
            url=member.display_avatar.url,
        )

        embed.set_image(url=member.display_avatar.url)
        return await ctx.reply(embed=embed)

    @commands.hybrid_command(aliases=["sav", "spfp", "pfp"])
    async def serveravatar(
        self,
        ctx: PretendContext,
        *,
        member: discord.Member = commands.Author,
    ):
        """
        Return someone's avatar
        """

        if member.guild_avatar is None:
            return await ctx.send_warning(f"**{member.name}** does not have a server avatar.")

        embed = discord.Embed(
            color=await self.bot.dominant_color(member.guild_avatar.url),
            title=f"{member.name}'s server avatar",
            url=member.guild_avatar.url,
        )

        embed.set_image(url=member.guild_avatar.url)
        return await ctx.reply(embed=embed)

    @commands.group(
        name="stickymessage",
        aliases=["stickymsg", "sticky"],
        invoke_without_command=True,
    )
    async def stickymessage(self, ctx: PretendContext):
        return await ctx.create_pages()

    @stickymessage.command(name="add", brief="manage guild")
    @has_guild_permissions(manage_guild=True)
    async def stickymessage_add(
        self, ctx: PretendContext, channel: TextChannel, *, code: str
    ):
        """add a sticky message to the server"""
        check = await self.bot.db.fetchrow(
            "SELECT * FROM stickymessage WHERE channel_id = $1", channel.id
        )
        if check:
            args = [
                "UPDATE stickymessage SET message = $1 WHERE channel_id = $2",
                code,
                channel.id,
            ]
        else:
            args = [
                "INSERT INTO stickymessage VALUES ($1,$2,$3)",
                ctx.guild.id,
                channel.id,
                code,
            ]

        await self.bot.db.execute(*args)
        return await ctx.send_success(
            f"Added sticky message to {channel.mention}\n```{code}```"
        )

    @stickymessage.command(name="remove", brief="manage guild")
    @has_guild_permissions(manage_guild=True)
    async def stickymessage_remove(self, ctx: PretendContext, *, channel: TextChannel):
        """remove a sticky message from the server"""
        check = await self.bot.db.fetchrow(
            "SELECT * FROM stickymessage WHERE channel_id = $1", channel.id
        )
        if not check:
            return await ctx.send_warning(
                "There is no sticky message configured in this channel"
            )

        await self.bot.db.execute(
            "DELETE FROM stickymessage WHERE channel_id = $1", channel.id
        )
        return await ctx.send_success(
            f"Deleted the sticky message from {channel.mention}"
        )

    @commands.command(aliases=["pastusernanes", "usernames", "oldnames", "pastnames"])
    async def names(self, ctx: PretendContext, *, user: discord.User = commands.Author):
        """
        Check a member's past usernames
        """

        results = await self.bot.db.fetch(
            "SELECT * FROM usernames WHERE user_id = $1", user.id
        )
        if len(results) == 0:
            return await ctx.send_error(
                f"{'You' if user == ctx.author else f'{user.mention}'} doesn't have **past usernames**"
            )

        users = sorted(results, key=lambda m: m["time"], reverse=True)

        return await ctx.paginate(
            [
                f"**{result['user_name']}** - {discord.utils.format_dt(datetime.datetime.fromtimestamp(result['time']), style='R')}"
                for result in users
            ],
            f"Username changes ({len(users)})",
            {"name": user.name, "icon_url": user.display_avatar.url},
        )

    @commands.command(aliases=["clearusernames", "deletenames", "deleteusernames"])
    async def clearnames(self, ctx: PretendContext):
        """clear your username history"""
        check = await self.bot.db.fetchrow(
            "SELECT * FROM usernames WHERE user_id = $1", ctx.author.id
        )
        if not check:
            return await ctx.send_warning("There are no usernames saved for you")

        async def yes_func(interaction: discord.Interaction):
            await self.bot.db.execute(
                "DELETE FROM usernames WHERE user_id = $1", interaction.user.id
            )
            return await interaction.response.edit_message(
                embed=discord.Embed(
                    color=self.bot.yes_color,
                    description=f"{self.bot.yes} {interaction.user.mention}: Cleared your username history",
                ),
                view=None,
            )

        async def no_func(interaction: discord.Interaction):
            return await interaction.response.edit_message(
                embed=discord.Embed(
                    color=self.bot.color,
                    description=f"{interaction.user.mention}: Aborting action",
                ),
                view=None,
            )

        await ctx.confirmation_send(
            "Are you sure you want to **clear** your username history?",
            yes_func,
            no_func,
        )

    @commands.hybrid_command()
    async def banner(
        self, ctx: PretendContext, *, member: discord.User = commands.Author
    ):
        """
        Get someone's banner
        """

        cache = self.bot.cache.get(f"profile-{member.id}")

        if cache:
            banner = cache["banner"]

            if banner is None:
                return await ctx.send_error(f"{member.mention} doesn't have a banner")

        else:
            user = await self.bot.fetch_user(member.id)

            if not user.banner:
                await self.cache_profile(user)
                return await ctx.send_error(f"{member.mention} doesn't have a banner")

            banner = user.banner.url

        embed = discord.Embed(
            color=await self.bot.dominant_color(banner),
            title=f"{member.name}'s banner",
            url=banner,
        )
        embed.set_image(url=banner)
        return await ctx.reply(embed=embed)

    @commands.hybrid_command(aliases=["ri"])
    async def roleinfo(
        self, ctx: PretendContext, *, role: Optional[discord.Role] = None
    ):
        """
        Information about a role
        """

        if role is None:
            role = ctx.author.top_role

        embed = (
            discord.Embed(
                color=role.color if role.color.value != 0 else self.bot.color,
                title=role.name,
            )
            .set_author(
                name=ctx.author.name,
                icon_url=(
                    role.display_icon
                    if isinstance(role.display_icon, discord.Asset)
                    else None
                ),
            )
            .add_field(name="Role ID", value=f"`{role.id}`")
            .add_field(
                name="Role color",
                value=(
                    f"`#{hex(role.color.value)[2:]}`"
                    if role.color.value != 0
                    else "No color"
                ),
            )
            .add_field(
                name="Created",
                value=f"{discord.utils.format_dt(role.created_at, style='f')} **{self.bot.humanize_date(role.created_at.replace(tzinfo=None))}**",
                inline=False,
            )
            .add_field(
                name=f"{len(role.members)} Member{'s' if len(role.members) != 1 else ''}",
                value=(
                    ", ".join([str(m) for m in role.members])
                    if len(role.members) < 7
                    else f"{', '.join([str(m) for m in role.members][:7])} + {len(role.members)-7} others"
                ),
                inline=False,
            )
        )
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="channelinfo", aliases=["ci"])
    async def channelinfo(
        self, ctx: PretendContext, *, channel: Optional[TextChannel] = None
    ):
        """
        view information about a channel
        """

        channel = channel or ctx.channel

        embed = (
            discord.Embed(color=self.bot.color, title=channel.name)
            .set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
            .add_field(name="Channel ID", value=f"`{channel.id}`", inline=True)
            .add_field(name="Type", value=str(channel.type), inline=True)
            .add_field(
                name="Guild",
                value=f"{channel.guild.name} (`{channel.guild.id}`)",
                inline=True,
            )
            .add_field(
                name="Category",
                value=f"{channel.category.name} (`{channel.category.id}`)",
                inline=False,
            )
            .add_field(name="Topic", value=channel.topic or "N/A", inline=True)
            .add_field(
                name="Created At",
                value=f"{discord.utils.format_dt(channel.created_at, style='F')} ({discord.utils.format_dt(channel.created_at, style='R')})",
                inline=False,
            )
        )

        await ctx.reply(embed=embed)

    @commands.command()
    async def donators(self, ctx: PretendContext):
        """
        Returns a list of all donators
        """

        results = await self.bot.db.fetch("SELECT * FROM donor")
        
        if len(results) == 0: 
            return await ctx.send_warning("There are **no** donors.") 
        
        res = sorted(results, key=lambda m: m["since"], reverse=True)
        return await ctx.paginate(
            [
                f"<@!{result['user_id']}> - <t:{int(result['since'])}:R> {'<a:0_boost15:1273206098337202207>' if result['status'] == 'boosted' else '💸'}"
                for result in res
            ],
            f"Pretend donators ({len(results)})",
        )

    @commands.hybrid_command()
    async def invites(
        self, ctx: PretendContext, *, member: discord.Member = commands.Author
    ):
        """
        returns the number of invites you have in the server
        """

        invites = await ctx.guild.invites()
        await ctx.pretend_send(
            f"{f'{member.mention} has' if member.id != ctx.author.id else 'You have'} **{sum(invite.uses for invite in invites if invite.inviter == member)} invites**"
        )

    @commands.command(aliases=["cs"], brief="manage messages")
    @commands.has_guild_permissions(manage_messages=True)
    async def clearsnipes(self, ctx: PretendContext):
        """
        Clear the snipes from the channel
        """

        for i in ["snipe", "edit_snipe", "reaction_snipe"]:
            snipes = self.bot.cache.get(i)

            if snipes:
                for s in [m for m in snipes if m["channel"] == ctx.channel.id]:
                    snipes.remove(s)
                await self.bot.cache.set(i, snipes)

        await ctx.send_success("Cleared all snipes from this channel")

    @commands.command(aliases=["rs"])
    async def reactionsnipe(self, ctx: PretendContext, index: int = 1):
        """
        Get the most recent message with a reaction removed in this channel
        """

        if not self.bot.cache.get("reaction_snipe"):
            return await ctx.send_warning("No reaction snipes found in this channel")

        snipes = [
            s
            for s in self.bot.cache.get("reaction_snipe")
            if s["channel"] == ctx.channel.id
        ]

        if len(snipes) == 0:
            return await ctx.send_warning("No reaction snipes found in this channel")

        if index > len(snipes):
            return await ctx.send_warning(
                f"There are only **{len(snipes)}** reaction snipes in this channel"
            )

        result = snipes[::-1][index - 1]
        try:
            message = await ctx.channel.fetch_message(result["message"])
            return await ctx.pretend_send(
                f"**{result['user']}** reacted with {result['reaction']} **{self.bot.humanize_date(datetime.datetime.fromtimestamp(int(result['created_at'])))}** [**here**]({message.jump_url})"
            )
        except:
            return await ctx.pretend_send(
                f"**{result['user']}** reacted with {result['reaction']} **{self.bot.humanize_date(datetime.datetime.fromtimestamp(int(result['created_at'])))}**"
            )

    @commands.command(aliases=["es"])
    async def editsnipe(self, ctx: PretendContext, index: int = 1):
        """
        Get the most recent edited message in the channel
        """

        if not self.bot.cache.get("edit_snipe"):
            return await ctx.send_warning("No edit snipes found in this channel")

        snipes = [
            s
            for s in self.bot.cache.get("edit_snipe")
            if s["channel"] == ctx.channel.id
        ]

        if len(snipes) == 0:
            return await ctx.send_warning("No edit snipes found in this channel")

        if index > len(snipes):
            return await ctx.send_warning(
                f"There are only **{len(snipes)}** edit snipes in this channel"
            )

        result = snipes[::-1][index - 1]
        embed = (
            discord.Embed(color=self.bot.color)
            .set_author(name=result["name"], icon_url=result["avatar"])
            .set_footer(text=f"{index}/{len(snipes)}")
        )

        for m in ["before", "after"]:
            embed.add_field(name=m, value=result[m])

        return await ctx.reply(embed=embed)

    @commands.command(aliases=["s"])
    async def snipe(self, ctx: PretendContext, index: int = 1):
        """
        Get the most recent deleted message in the channel
        """
        try:
            if not self.bot.cache.get("snipe"):
                return await ctx.send_warning("No snipes found in this channel")
            snipes = [
                s for s in self.bot.cache.get("snipe") if s["channel"] == ctx.channel.id
            ]
            if len(snipes) == 0:
                return await ctx.send_warning("No snipes found in this channel")
            if index > len(snipes):
                return await ctx.send_warning(
                    f"There are only **{len(snipes)}** snipes in this channel"
                )
            result = snipes[::-1][index - 1]
            embed = (
                discord.Embed(
                    color=self.bot.color,
                    description=result["message"],
                    timestamp=datetime.datetime.fromtimestamp(
                        result["created_at"]
                    ).replace(tzinfo=None),
                )
                .set_author(name=result["name"], icon_url=result["avatar"])
                .set_footer(text=f"{index}/{len(snipes)}")
            )

            if len(result["stickers"]) > 0:
                sticker: discord.StickerItem = result["stickers"][0]
                embed.set_image(url=sticker.url)
            else:
                if len(result["attachments"]) > 0:
                    attachment: discord.Attachment = result["attachments"][0]
                    if ".mp4" in attachment.filename or ".mov" in attachment.filename:
                        file = discord.File(
                            BytesIO(await attachment.read()),
                            filename=attachment.filename,
                        )
                        return await ctx.reply(embed=embed, file=file)
                    else:
                        embed.set_image(url=attachment.url)

            return await ctx.reply(embed=embed)
        except Exception as e:
            return await ctx.send_warning("There was an error getting snipes.")

    @commands.hybrid_command(aliases=["mc"])
    async def membercount(self, ctx: PretendContext, invite: discord.Invite = None):
        """
        Returns the number of members in your server or the server given
        """

        if invite:
            embed = discord.Embed(
                color=self.bot.color,
                description=f"> **members:** {invite.approximate_member_count:,}",
            ).set_author(
                name=f"{invite.guild.name}'s statistics", icon_url=invite.guild.icon
            )
        else:
            embed = discord.Embed(
                color=self.bot.color,
                description=f">>> **humans** - {len(set(m for m in ctx.guild.members if not m.bot)):,}\n**bots** - {len(set(m for m in ctx.guild.members if m.bot)):,}\n**total** - {ctx.guild.member_count:,}",
            ).set_author(
                icon_url=ctx.guild.icon,
                name=f"{ctx.guild.name}'s statistics (+{len([m for m in ctx.guild.members if (datetime.datetime.now() - m.joined_at.replace(tzinfo=None)).total_seconds() < 3600*24])})",
            )

        return await ctx.reply(embed=embed)

    @commands.hybrid_command(aliases=["si"])
    async def serverinfo(self, ctx: PretendContext, invite: discord.Invite = None):
        """
        Get the information about a server
        """

        if invite:
            embed = discord.Embed(
                color=self.bot.color, title=f"Invite code: {invite.code}"
            ).add_field(
                name="Invite",
                value=f"**channel:** {invite.channel.name} ({invite.channel.type})\n**id:** `{invite.channel.id}`\n**expires:** {f'yes ({self.bot.humanize_date(invite.expires_at.replace(tzinfo=None))})' if invite.expires_at else 'no'}\n**uses:** {invite.uses or 'unknown'}",
            )

            if invite.guild:
                embed.description = invite.guild.description or ""
                embed.set_thumbnail(url=invite.guild.icon).add_field(
                    name="Server",
                    value=f"**name:** {invite.guild.name}\n**id:** `{invite.guild.id}`\n**members:** {invite.approximate_member_count:,}\n**created**: {discord.utils.format_dt(invite.created_at, style='R') if invite.created_at else 'N/A'}",
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
                .set_author(
                    name=f"{ctx.guild.owner} ({ctx.guild.owner_id})",
                    icon_url=ctx.guild.owner.display_avatar.url,
                )
                .set_thumbnail(url=ctx.guild.icon)
                .add_field(
                    name="Counts",
                    value=f">>> **Roles:** {len(ctx.guild.roles):,}\n**Emojis:** {len(ctx.guild.emojis):,}\n**Stickers:** {len(ctx.guild.stickers):,}",
                )
                .add_field(
                    name="Members",
                    value=f">>> **Users:** {len(set(i for i in ctx.guild.members if not i.bot)):,}\n**Bots:** {len(set(i for i in ctx.guild.members if i.bot)):,}\n**Total:** {ctx.guild.member_count:,}",
                )
                .add_field(
                    name="Channels",
                    value=f">>> **Text:** {len(ctx.guild.text_channels):,}\n**Voice:** {len(ctx.guild.voice_channels):,}\n**Categories:** {len(ctx.guild.categories):,}",
                )
                .add_field(
                    name="Info",
                    value=f">>> **Vanity:** {ctx.guild.vanity_url_code or 'N/A'}\n**Popularity:** {servers.index(ctx.guild)+1}/{len(self.bot.guilds)}",
                )
            )
            embed.add_field(
                name="Boost",
                value=f">>> **Boosts:** {ctx.guild.premium_subscription_count:,}\n**Level:** {ctx.guild.premium_tier}\n**Boosters:** {len(ctx.guild.premium_subscribers)}",
            ).add_field(
                name="Design",
                value=f">>> **Icon:** {f'[**here**]({ctx.guild.icon})' if ctx.guild.icon else 'N/A'}\n**Banner:**  {f'[**here**]({ctx.guild.banner})' if ctx.guild.banner else 'N/A'}\n**Splash:**  {f'[**here**]({ctx.guild.splash})' if ctx.guild.splash else 'N/A'}",
            ).set_footer(
                text=f"Guild ID: {ctx.guild.id} • Shard: {ctx.guild.shard_id}/{len(self.bot.shards)}"
            )

        await ctx.reply(embed=embed)

    @commands.command(aliases=["user", "ui", "whois"])
    async def userinfo(
        self,
        ctx,
        *,
        member: Union[discord.Member, discord.User] = commands.Author,
    ):
        """
        Returns information about an user
        """

        def vc(mem: discord.Member):
            if mem.voice:
                channelname = mem.voice.channel.name
                deaf = (
                    "<:undeafened:1258833442758594622>"
                    if mem.voice.self_deaf or mem.voice.deaf
                    else "<:undeafened:1258833442758594622> "
                )
                mute = (
                    "<:unmuted:1258832911981875330>"
                    if mem.voice.self_mute or mem.voice.mute
                    else "<:unmuted:1258832911981875330>"
                )
                stream = (
                    "<:stream:1258832920345579621>" if mem.voice.self_stream else ""
                )
                video = "<:rename:1258832924737015958>" if mem.voice.self_video else ""
                channelmembers = (
                    f"with {len(mem.voice.channel.members)-1} other member{'s' if len(mem.voice.channel.members) > 2 else ''}"
                    if len(mem.voice.channel.members) > 1
                    else ""
                )
                return f" {deaf} {mute} {stream} {video} **in voice channel** {channelname} {channelmembers}\n"
            return ""

        embed = (
            discord.Embed(
                color=self.bot.color,
                description=f"**{member}**",
            )
            .set_author(
                name=f"{member.name} ({member.id})", icon_url=member.display_avatar.url
            )
            .set_thumbnail(url=member.display_avatar.url)
            .add_field(
                name="Created",
                value=f"{discord.utils.format_dt(member.created_at, style='D')}\n{discord.utils.format_dt(member.created_at, style='R')}",
            )
        )

        if not isinstance(member, discord.ClientUser):
            embed.set_footer(text=f"{len(member.mutual_guilds):,} server(s)")

        if isinstance(member, discord.Member):
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            embed.description += vc(member)

            if not isinstance(member, discord.ClientUser):
                embed.set_footer(
                    text=f"Join position: {members.index(member)+1:,}, {len(member.mutual_guilds):,} server(s)"
                )

            embed.add_field(
                name="Joined",
                value=f"{discord.utils.format_dt(member.joined_at, style='D')}\n{discord.utils.format_dt(member.joined_at, style='R')}",
            )

            if member.premium_since:
                embed.add_field(
                    name="Boosted",
                    value=f"{discord.utils.format_dt(member.premium_since, style='D')}\n{discord.utils.format_dt(member.premium_since, style='R')}",
                )

            roles = member.roles[1:][::-1]

            if len(roles) > 0:
                embed.add_field(
                    name=f"Roles ({len(roles)})",
                    value=" ".join([r.mention for r in roles])
                    if len(roles) < 5
                    else " ".join([r.mention for r in roles[:4]])
                    + f" ... and {len(roles)-4} more",
                    inline=False,
                )

        await ctx.send(embed=embed)


#    @commands.hybrid_command()
#    async def weather(self, ctx: PretendContext, *, location: WeatherLocation):
#        """
#        Returns the weather of a location
#        """
#
#        embed = (
#            discord.Embed(
#                color=self.bot.color,
#                title=f"{location.condition} in {location.place}, {location.country}",
#                timestamp=location.time,
#            )
#            .set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
#            .set_thumbnail(url=location.condition_image)
#            .add_field(
#                name="Temperature",
#                value=f"{location.temp_c} °C / {location.temp_f} °F",
#                inline=False,
#            )
#            .add_field(name="Humidity", value=f"{location.humidity}%", inline=False)
#            .add_field(
#                name="Wind",
#                value=f"{location.wind_mph} mph / {location.wind_kph} kph",
#                inline=False,
#            )
#        )
#
#        return await ctx.reply(embed=embed)
#
#    @commands.hybrid_command()
#    async def roblox(self, ctx: PretendContext, user: RobloxUser):
#        """
#        Get someone's roblox profile
#        """
#
#        embed = (
#            discord.Embed(
#                color=self.bot.color,
#                title=f"{user.display_name} @{user.username}",
#                url=user.url,
#                description=user.bio,
#            )
#            .set_thumbnail(url=user.avatar_url)
#            .add_field(name="Friends", value=user.friends)
#            .add_field(name="Followers", value=user.followers)
#            .add_field(name="Following", value=user.followings)
#            .set_footer(text=self.get_joined_date(user.created_at), icon_url=user.icon)
#        )
#
#        if user.banned:
#            embed.set_author(name="This user is banned")
#
#        await ctx.reply(embed=embed)
#
#    @commands.hybrid_command(aliases=["snap"])
#    async def snapchat(self, ctx: PretendContext, user: SnapUser):
#        """
#        Get someone's snapchat profile
#        """
#
#        embed = (
#            discord.Embed(
#                color=self.bot.color,
#                title=user.display_name,
#                url=user.url,
#                description=user.bio,
#            )
#            .set_author(name=user.username)
#            .set_thumbnail(url=user.avatar)
#        )
#
#        button = discord.ui.Button(
#            label="snapcode", emoji="<:snap:1142555339133300917>"
#        )
#
#        async def button_callback(interaction: discord.Interaction):
#            e = discord.Embed(color=0xFFFF00)
#            e.set_image(url=user.snapcode)
#            await interaction.response.send_message(embed=e, ephemeral=True)
#
#        button.callback = button_callback
#        view = discord.ui.View()
#        view.add_item(button)
#
#        await ctx.reply(embed=embed, view=view)
#
#    @commands.hybrid_command(aliases=["snapstory"])
#    async def snapchatstory(self, ctx: PretendContext, *, username: str):
#        """
#        Get someone's snapchat stories
#        """
#
#        results = await self.bot.session.get_json(
#            "https://v1.pretend.bot/snapstory",
#            headers={"api-key": self.bot.pretend_api},
#            params={"username": username},
#        )
#
#        if results.get("detail"):
#            return await ctx.send_error(results["detail"])
#
#        await ctx.paginator(list(map(lambda s: s["url"], results["stories"])))
#
#    @commands.hybrid_command(aliases=["ig"])
#    async def instagram(self, ctx: PretendContext, *, user: InstagramUser):
#        """
#        Get someone's instagram profile
#        """
#
#        embed = (
#            discord.Embed(
#                color=self.bot.color,
#                title=f"@{user.username}",
#                description=user.bio,
#                url=user.url,
#            )
#            .set_thumbnail(url=user.profile_pic)
#            .add_field(name="Following", value=f"{user.following:,}")
#            .add_field(name="Followers", value=f"{user.followers:,}")
#            .add_field(name="Posts", value=f"{user.posts:,}")
#        )
#
#        if user.pronouns:
#            embed.set_author(name=", ".join(user.pronouns))
#
#        return await ctx.reply(embed=embed)
#
#    @commands.hybrid_command(aliases=["tt"])
#    async def tiktok(self, ctx: PretendContext, *, user: TikTokUser):
#        """
#        Get someone's tiktok profile
#        """
#
#        embed = (
#            discord.Embed(
#                color=self.bot.color,
#                url=user.url,
#                title=(
#                    f"{f'{user.nickname} ({user.username})' if user.nickname else f'{user.username}'} {''.join(user.badges)}"
#                    if user.nickname != "⠀⠀"
#                    else f"{user.username} {''.join(user.badges)}"
#                ),
#                description=user.bio,
#            )
#            .set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
#            .set_thumbnail(url=user.avatar)
#            .add_field(name="Following", value=f"{user.following:,}")
#            .add_field(name="Followers", value=f"{user.followers:,}")
#            .add_field(name="Hearts", value=f"{user.hearts:,}")
#        )
#        await ctx.reply(embed=embed)
#
#    @commands.hybrid_command(aliases=["git"])
#    async def github(self, ctx: PretendContext, *, user: GithubUser):
#        """
#        Get someone's github profile
#        """
#
#        embed = (
#            discord.Embed(
#                color=self.bot.color,
#                title=f"{user.username} {f'aka {user.display}' if user.display else ''}",
#                description=user.bio,
#                url=user.url,
#                timestamp=user.created_at,
#            )
#            .set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
#            .set_thumbnail(url=user.avatar_url)
#            .add_field(name="Followers", value=user.followers)
#            .add_field(name="Following", value=user.following)
#            .add_field(name="Repos", value=user.repos)
#        )
#
#        await ctx.reply(embed=embed)

    @commands.hybrid_command(aliases=["fnshop"])
    async def fortniteshop(self, ctx: PretendContext):
        """
        Get the fortnite item shop for today
        """

        now = datetime.datetime.now()
        file = discord.File(
            await self.bot.getbyte(
                f"https://bot.fnbr.co/shop-image/fnbr-shop-{now.day}-{now.month}-{now.year}.png"
            ),
            filename="fortnite.png",
        )

        await ctx.send(file=file)

    @commands.command(aliases=["splash"])
    async def serversplash(
        self, ctx: PretendContext, *, invite: Optional[discord.Invite] = None
    ):
        """
        Get a server's splash
        """

        if invite:
            guild = invite.guild
        else:
            guild = ctx.guild

        if not guild.splash:
            return await ctx.send_error("This server has no splash image")

        embed = discord.Embed(
            color=await self.bot.dominant_color(guild.splash.url),
            title=f"{guild.name}'s splash",
            url=guild.splash.url,
        ).set_image(url=guild.splash.url)

        await ctx.reply(embed=embed)

    @commands.command(aliases=["sbanner"])
    async def serverbanner(
        self, ctx: PretendContext, *, invite: Optional[discord.Invite] = None
    ):
        """
        Get a server's banner
        """

        if invite:
            guild = invite.guild
        else:
            guild = ctx.guild

        if not guild.banner:
            return await ctx.send_error("This server has no banner")

        embed = discord.Embed(
            color=await self.bot.dominant_color(guild.banner.url),
            title=f"{guild.name}'s banner",
            url=guild.banner.url,
        ).set_image(url=guild.banner.url)

        await ctx.reply(embed=embed)

    @commands.command(aliases=["sicon"])
    async def servericon(
        self, ctx: PretendContext, *, invite: Optional[discord.Invite] = None
    ):
        """
        Get a server's icon
        """

        if invite:
            guild = invite.guild
        else:
            guild = ctx.guild

        if not guild.icon:
            return await ctx.send_error("This server has no icon")

        embed = discord.Embed(
            color=await self.bot.dominant_color(guild.icon.url),
            title=f"{guild.name}'s icon",
            url=guild.icon.url,
        ).set_image(url=guild.icon.url)

        await ctx.reply(embed=embed)

    @commands.hybrid_command(aliases=["define"])
    async def urban(self, ctx: PretendContext, *, word: str):
        """
        find a definition of a word
        """

        embeds = []

        data = await self.bot.session.get_json(
            "http://api.urbandictionary.com/v0/define", params={"term": word}
        )

        defs = data["list"]
        if len(defs) == 0:
            return await ctx.send_error(f"No definition found for **{word}**")

        for defi in defs:
            e = (
                discord.Embed(
                    color=self.bot.color,
                    title=word,
                    description=defi["definition"],
                    url=defi["permalink"],
                    timestamp=dateutil.parser.parse(defi["written_on"]),
                )
                .set_author(
                    name=ctx.author.name, icon_url=ctx.author.display_avatar.url
                )
                .add_field(name="example", value=defi["example"], inline=False)
                .set_footer(text=f"{defs.index(defi)+1}/{len(defs)}")
            )
            embeds.append(e)

        return await ctx.paginator(embeds)

#    @commands.command(aliases=["tr"])
#    async def translate(self, ctx: PretendContext, language: str, *, message: str):
#        """
#        Translate a message to a specific language
#        """
#
#        try:
#            translator = GoogleTranslator(source="auto", target=language)
#            translated = await self.bot.loop.run_in_executor(
#                self.bot.executor, translator.translate, message
#            )
#            embed = discord.Embed(
#                color=self.bot.color,
#                title=f"translated to {language}",
#                description=f"```{translated}```",
#            )
#
#            await ctx.reply(embed=embed)
#        except LanguageNotSupportedException:
#            return await ctx.send_error("This language is **not** supported")

    @commands.hybrid_command()
    async def seen(
        self, ctx: PretendContext, *, member: discord.Member = commands.Author
    ):
        """
        Check when a member was last seen
        """

        time = await self.bot.db.fetchval(
            """
      SELECT time FROM seen
      WHERE user_id = $1
      AND guild_id = $2
      """,
            member.id,
            ctx.guild.id,
        )

        if not time:
            return await ctx.send_error("This member doesn't have any last seen record")

        await ctx.pretend_send(
            f"**{member}** was last seen **{self.bot.humanize_date(datetime.datetime.fromtimestamp(time.timestamp()))}**"
        )

    @commands.hybrid_command()
    @is_afk()
    async def afk(self, ctx: PretendContext, *, reason: str = "AFK"):
        """
        let the members know that you're away
        """

        await self.bot.db.execute(
            """
      INSERT INTO afk
      VALUES ($1,$2,$3,$4)
      """,
            ctx.guild.id,
            ctx.author.id,
            reason,
            datetime.datetime.now(),
        )

        embed = discord.Embed(
            color=self.bot.color,
            description=f"😴 {ctx.author.mention}: You are now AFK with the reason: **{reason}**",
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=["hex"])
    async def dominant(self, ctx: PretendContext):
        """
        Get the color of an image
        """

        attachment = await ctx.get_attachment()

        if not attachment:
            return await ctx.send_help("dominant")

        color = hex(await self.bot.dominant_color(attachment.url))[2:]
        hex_info = await self.bot.session.get_json(
            "https://www.thecolorapi.com/id", params={"hex": color}
        )
        hex_image = f"https://singlecolorimage.com/get/{color}/200x200"
        embed = (
            discord.Embed(color=int(color, 16))
            .set_author(icon_url=hex_image, name=hex_info["name"]["value"])
            .set_thumbnail(url=hex_image)
            .add_field(name="RGB", value=hex_info["rgb"]["value"])
            .add_field(name="HEX", value=hex_info["hex"]["value"])
        )

        await ctx.reply(embed=embed)

    @commands.command()
    async def youngest(self, ctx: PretendContext):
        """
        Get the youngest account in the server
        """

        member = (
            sorted(
                [m for m in ctx.guild.members if not m.bot],
                key=lambda m: m.created_at,
                reverse=True,
            )
        )[0]

        embed = (
            discord.Embed(
                color=self.bot.color,
                title=f"Youngest account in {ctx.guild.name}",
                url=f"https://discord.com/users/{member.id}",
            )
            .add_field(name="user", value=member.mention)
            .add_field(
                name="created",
                value=self.bot.humanize_date(member.created_at.replace(tzinfo=None)),
            )
        )
        await ctx.reply(embed=embed)

    @commands.command()
    async def oldest(self, ctx: PretendContext):
        """
        Get the oldest account in the server
        """

        member = (
            sorted(
                [m for m in ctx.guild.members if not m.bot], key=lambda m: m.created_at
            )
        )[0]
        embed = (
            discord.Embed(
                color=self.bot.color,
                title=f"Oldest account in {ctx.guild.name}",
                url=f"https://discord.com/users/{member.id}",
            )
            .add_field(name="user", value=member.mention)
            .add_field(
                name="created",
                value=self.bot.humanize_date(member.created_at.replace(tzinfo=None)),
            )
        )

        await ctx.reply(embed=embed)

    @commands.hybrid_command(brief="manage messages", aliases=["pic"])
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def picperms(
        self,
        ctx: PretendContext,
        member: discord.Member,
        *,
        channel: discord.TextChannel = commands.CurrentChannel,
    ):
        """
        Give a member permissions to post attachments in a channel
        """

        overwrite = channel.overwrites_for(member)

        if (
            channel.permissions_for(member).attach_files
            and channel.permissions_for(member).embed_links
        ):
            overwrite.attach_files = False
            overwrite.embed_links = False
            await channel.set_permissions(
                member,
                overwrite=overwrite,
                reason=f"Picture permissions removed by {ctx.author}",
            )
            return await ctx.send_success(
                f"Removed pic perms from {member.mention} in {channel.mention}"
            )
        else:
            overwrite.attach_files = True
            overwrite.embed_links = True
            await channel.set_permissions(
                member,
                overwrite=overwrite,
                reason=f"Picture permissions granted by {ctx.author}",
            )
            return await ctx.send_success(
                f"Added pic perms to {member.mention} in {channel.mention}"
            )

    @commands.command()
    async def roles(self, ctx: PretendContext):
        """
        Returns a list of server's roles
        """

        role_list = [
            f"{role.mention} - {len(role.members)} member{'s' if len(role.members) != 1 else ''}"
            for role in ctx.guild.roles[1:][::-1]
        ]
        return await ctx.paginate(
            role_list,
            f"Roles in {ctx.guild.name} ({len(ctx.guild.roles[1:])})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.command()
    async def muted(self, ctx: PretendContext):
        """
        Returns a list of muted members
        """

        members = [
            f"{member.mention} - {discord.utils.format_dt(member.timed_out_until, style='R')}"
            for member in ctx.guild.members
            if member.timed_out_until
        ]

        if len(members) == 0:
            return await ctx.send_warning("There are **no** muted members.")

        return await ctx.paginate(
            members,
            f"Muted in {ctx.guild.name} ({len(members)})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.command()
    async def joins(self, ctx: PretendContext):
        """
        Returns a list of members that joined in the last 24 hours
        """

        members = sorted(
            [
                m
                for m in ctx.guild.members
                if (
                    datetime.datetime.now() - m.joined_at.replace(tzinfo=None)
                ).total_seconds()
                < 3600 * 24
            ],
            key=lambda m: m.joined_at,
            reverse=True,
        )

        if len(members) == 0:
            return await ctx.send_warning("There are **no** new members.")

        return await ctx.paginate(
            [
                f"{m} - {discord.utils.format_dt(m.joined_at, style='R')}"
                for m in members
            ],
            f"Joined today ({len(members)})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def bans(self, ctx: PretendContext):
        """
        Returns a list of banned users
        """

        banned = [ban async for ban in ctx.guild.bans(limit=100)]
        
        if not banned: 
            return await ctx.send_warning("There is **no** banned members.")

        return await ctx.paginate(
            [f"{m.user} - {m.reason or 'no reason'}" for m in banned],
            f"Bans ({len(banned)})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.command()
    async def bots(self, ctx: PretendContext):
        """
        Returns a list of all bots in this server
        """

        return await ctx.paginate(
            [f"{m.mention} `{m.id}`" for m in ctx.guild.members if m.bot],
            f"Bots ({len([m for m in ctx.guild.members if m.bot])})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.command()
    async def boosters(self, ctx: PretendContext):
        """
        Returns a list of members that boosted the server
        """

        members = sorted(
            ctx.guild.premium_subscribers, key=lambda m: m.premium_since, reverse=True
        )

        if not members: 
            return await ctx.send_warning("There is **no** boosters.")

        return await ctx.paginate(
            [
                f"{m} - {discord.utils.format_dt(m.premium_since, style='R')}"
                for m in members
            ],
            f"Boosters ({len(ctx.guild.premium_subscribers)})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.command()
    async def inrole(self, ctx: PretendContext, *, role: Union[discord.Role, str]):
        """
        Get the list of members that have a specific
        """

        if isinstance(role, str):
            role = ctx.find_role(role)
            if not role:
                return await ctx.send_error("Role not found")

        if len(role.members) > 200:
            return await ctx.send_warning(
                "Cannot view roles with more than **200** members"
            )

        return await ctx.paginate(
            [f"{m} (`{m.id}`)" for m in role.members],
            f"Members with {role.name} ({len(role.members)})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.command()
    async def shazam(self, ctx: PretendContext):
        """
        Get the name of a music in a file using shazam
        """

        attachment = await ctx.get_attachment()

        if not attachment:
            await ctx.send_help(ctx.command)

        embed = discord.Embed(
            color=0x09A1ED,
            description=f"<:shazam:1272353421567201331> {ctx.author.mention}: Searching for track...",
        )

        mes = await ctx.reply(embed=embed)
        
        try:
            out = await Shazam().recognize_song(await attachment.read())
            track = out["track"]["share"]["text"]
            link = out["track"]["share"]["href"]

            embed = discord.Embed(
                color=0x09A1ED,
                description=f"<:shazam:1272353421567201331> {ctx.author.mention}: Found [**{track}**]({link})",
            )

            await mes.edit(embed=embed)
        
        except:
            embed = discord.Embed(
                color=self.bot.no_color,
                description=f"{self.bot.no} {ctx.author.mention}: Unable to find this attachment's track name",
            )

            await mes.edit(embed=embed)

#    @commands.command(aliases=["ca"])
#    async def cashapp(self, ctx: PretendContext, user: CashappUser):
#        """
#        get someone's cashapp url and qr
#        """
#
#        await ctx.send(user.url, file=discord.File(user.qr, filename="cashapp_qr.png"))
#
    @commands.group(aliases=["tz"], invoke_without_command=True)
    async def timezone(
        self, ctx: PretendContext, *, member: Optional[TimezoneMember] = None
    ):
        """
        Get the member's current date
        """

        if member is None:
            member = await TimezoneMember().convert(ctx, str(ctx.author))

        embed = discord.Embed(
            color=self.bot.color,
            description=f"🕑 {ctx.author.mention}: **{member[0].name}'s** current date **{member[1]}**",
        )
        await ctx.send(embed=embed)

    @timezone.command(name="set")
    async def timezone_set(self, ctx: PretendContext, *, timezone: TimezoneLocation):
        """
        Set your timezone
        """

        embed = discord.Embed(
            color=self.bot.color,
            description=f"Saved your timezone as **{timezone.timezone}**\n🕑 Current date: **{timezone.date}**",
        )
        await ctx.send(embed=embed)

    @timezone.command(name="unset")
    async def timezone_unset(self, ctx: PretendContext):
        """
        Unset your timezone
        """

        await self.bot.db.execute(
            """
      DELETE FROM timezone
      WHERE user_id = $1
      """,
            ctx.author.id,
        )

        return await ctx.send_success(f"You succesfully deleted your timezone")

    @timezone.command(name="list")
    async def timezone_list(self, ctx: PretendContext):
        """
        Get the timezones of everyone in this server
        """

        ids = list(map(lambda m: str(m.id), ctx.guild.members))
        results = await self.bot.db.fetch(
            f"SELECT zone, user_id FROM timezone WHERE user_id IN ({', '.join(ids)})"
        )
        await ctx.paginate(
            [
                f"<@{result['user_id']}> - **{await self.tz.get_timezone(ctx.guild.get_member(result['user_id']))}"
                for result in results
            ],
            f"Timezones ({len(results)})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.group(aliases=["bday"], invoke_without_command=True)
    async def birthday(
        self, ctx: PretendContext, *, member: Optional[BdayMember] = None
    ):
        """
        Get the birthday of an user
        """

        if member is None:
            member = await BdayMember().convert(ctx, str(ctx.author))

        embed = discord.Embed(
            color=0xDEA5A4,
            description=f"🎂 {ctx.author.mention}: **{member.name}'s** birthday is **{member.date}**. That's **{member.birthday}**",
        )

        await ctx.reply(embed=embed)

    @birthday.command(name="set")
    async def bday_set(self, ctx: PretendContext, *, date: BdayDate):
        """
        Set your birthday
        """

        embed = discord.Embed(
            color=0xDEA5A4,
            description=f"🎂 Your birthday is **{date[0]}**. That's **{date[1]}**",
        )
        await ctx.reply(embed=embed)

    @birthday.command(name="unset")
    async def bday_unset(self, ctx: PretendContext):
        """
        Unset your birthday
        """

        await self.bot.db.execute(
            """
      DELETE FROM bday
      WHERE user_id = $1
      """,
            ctx.author.id,
        )

        return await ctx.send_success(f"You succesfully deleted your birthday")

    @birthday.command(name="list")
    async def bday_list(self, ctx: PretendContext):
        """
        Get the birthdays of everyone in this server
        """

        ids = list(map(lambda m: str(m.id), ctx.guild.members))
        results = await self.bot.db.fetch(
            f"SELECT * FROM bday WHERE user_id IN ({', '.join(ids)})"
        )

        if len(results) == 0: 
            return await ctx.send_warning("There is **no one** with their birthday set.")
        
        await ctx.paginate(
            [
                f"""<@{result['user_id']}> - **{self.tz.months.get(result['month'])} {result['day']}**"""
                for result in results
            ],
            f"Birthdays ({len(results)})",
            {"name": ctx.guild.name, "icon_url": ctx.guild.icon},
        )

    @commands.group(invoke_without_command=True)
    async def reminder(self, ctx):
        return await ctx.create_pages()

    @reminder.command(name="add")
    @reminder_exists()
    async def reminder_add(self, ctx: PretendContext, time: ValidTime, *, task: str):
        """
        Make the bot remind you about a task
        """

        if time < 60:
            return await ctx.send_warning("Reminder time can't be less than a minute")

        else:
            try:
                await self.bot.db.execute(
                    """
        INSERT INTO reminder
        VALUES ($1,$2,$3,$4,$5)
        """,
                    ctx.author.id,
                    ctx.channel.id,
                    ctx.guild.id,
                    (datetime.datetime.now() + datetime.timedelta(seconds=time)),
                    task,
                )

                await ctx.send(
                    f"🕰️ {ctx.author.mention}: I'm going to remind you in {humanfriendly.format_timespan(time)} about **{task}**"
                )
            except:
                return await ctx.send_warning(
                    f"You already have a reminder set in this channel. Use `{ctx.clean_prefix}reminder stop` to cancel the reminder"
                )

    @reminder.command(name="stop", aliases=["cancel"])
    @is_there_a_reminder()
    async def reminder_stop(self, ctx: PretendContext):
        """
        Stop the bot from reminding you
        """

        await self.bot.db.execute(
            """
      DELETE FROM reminder
      WHERE guild_id = $1
      AND user_id = $2
      """,
            ctx.guild.id,
            ctx.author.id,
        )

        return await ctx.send_success("Deleted a reminder")

    @commands.command(aliases=["remindme"])
    @reminder_exists()
    async def remind(self, ctx: PretendContext, time: ValidTime, *, task: str):
        """
        Make the bot remind you about a task
        """

        if time < 60:
            return await ctx.send_warning("Reminder time can't be less than a minute")
        else:
            try:
                await self.bot.db.execute(
                    """
        INSERT INTO reminder
        VALUES ($1,$2,$3,$4,$5)
        """,
                    ctx.author.id,
                    ctx.channel.id,
                    ctx.guild.id,
                    (datetime.datetime.now() + datetime.timedelta(seconds=time)),
                    task,
                )
                await ctx.send(
                    f"🕰️ {ctx.author.mention}: I'm going to remind you in {humanfriendly.format_timespan(time)} about **{task}**"
                )
            except:
                return await ctx.send_warning(
                    f"You already have a reminder set in this channel. Use `{ctx.clean_prefix}reminder stop` to cancel the reminder"
                )

    @commands.group(name="tag", aliases=["tags", "t"], invoke_without_command=True)
    async def tag(self, ctx: PretendContext, *, tag: str):
        """
        view a tag
        """

        check = await self.bot.db.fetchrow(
            """
      SELECT * FROM tags
      WHERE guild_id = $1
      AND name = $2
      """,
            ctx.guild.id,
            tag,
        )

        if not check:
            return await ctx.send_warning(f"No tag found for **{tag}**")

        x = await self.bot.embed_build.convert(ctx, check["response"])
        await ctx.send(**x)

    @tag.command(name="create", aliases=["make"], brief="manage server")
    @commands.has_guild_permissions(manage_guild=True)
    async def tag_create(self, ctx: PretendContext, *, args: str):
        """
        create a tag
        """

        args = args.split(",", maxsplit=1)

        if len(args) == 1:
            return await ctx.send_warning(
                "No response found. Make sure to use a `,` to split the trigger from the response"
            )

        name = args[0]
        response = args[1].strip()

        if await self.bot.db.fetchrow(
            """
      SELECT * FROM tags
      WHERE guild_id = $1
      AND name = $2
      """,
            ctx.guild.id,
            name,
        ):
            return await ctx.send_warning(f"A tag for **{name}** already exists!")

        await self.bot.db.execute(
            """
      INSERT INTO tags
      VALUES ($1, $2, $3, $4)
      """,
            ctx.guild.id,
            ctx.author.id,
            name,
            response,
        )
        await ctx.send_success(f"Added tag for **{name}**" + f"\n```{response}```")

    @tag.command(name="remove", aliases=["delete", "del"], brief="manage server")
    @commands.has_guild_permissions(manage_guild=True)
    async def tag_remove(self, ctx: PretendContext, *, tag: str):
        """
        delete a tag
        """

        if not await self.bot.db.fetchrow(
            """
      SELECT * FROM tags
      WHERE guild_id = $1
      AND name = $2
      """,
            ctx.guild.id,
            tag,
        ):
            return await ctx.send_warning(f"That is **not** an existing tag")

        await self.bot.db.execute(
            """
      DELETE FROM tags
      WHERE guild_id = $1
      AND name = $2
      """,
            ctx.guild.id,
            tag,
        )
        await ctx.send_success(f"Deleted the tag **{tag}**")

    @tag.command(name="reset", brief="manage server")
    @commands.has_guild_permissions(manage_guild=True)
    async def tag_reset(self, ctx: PretendContext):
        """
        delete all tags in the guild
        """

        if not await self.bot.db.fetchrow(
            """
      SELECT * FROM tags
      WHERE guild_id = $1
      """,
            ctx.guild.id,
        ):
            return await ctx.send_warning(f"There are **no** tags set")

        async def yes_func(interaction: discord.Interaction):
            await self.bot.db.execute(
                """
        DELETE FROM tags
        WHERE guild_id = $1
        """,
                interaction.guild.id,
            )
            await interaction.response.edit_message(
                embed=discord.Embed(
                    description=f"{self.bot.yes} {interaction.user.mention}: Removed all **tags**",
                    color=self.bot.yes_color,
                ),
                view=None,
            )

        async def no_func(interaction: discord.Interaction):
            await interaction.response.edit_message(
                embed=discord.Embed(
                    description=f"{interaction.user.mention}: Cancelling action...",
                    color=self.bot.color,
                ),
                view=None,
            )

        await ctx.confirmation_send(
            f"Are you sure you want to **delete** all tags?", yes_func, no_func
        )

    @tag.command(name="list", brief="manage server")
    @commands.has_guild_permissions(manage_guild=True)
    async def tag_list(self, ctx: PretendContext):
        """
        returns a list of all tags
        """

        results = await self.bot.db.fetch(
            """
            SELECT * FROM tags
            WHERE guild_id = $1
            """,
            ctx.guild.id,
        )

        if not results:
            return await ctx.send_warning(f"There are **no** tags set")

        await ctx.paginate(
            [f"{result['name']} - {result['response']}" for result in results],
            title=f"Tags ({len(results)})",
            author={"name": ctx.guild.name, "icon_url": ctx.guild.icon or None},
        )

    @tag.command(name="random")
    async def tag_random(self, ctx: PretendContext):
        """
        returns a random tag from the guild
        """

        result = await self.bot.db.fetchrow(
            """
            SELECT * FROM tags
            WHERE guild_id = $1
            ORDER BY RANDOM()
            LIMIT 1
            """,
            ctx.guild.id,
        )

        if not result:
            return await ctx.send_warning(f"There are **no** tags set")

        x = await self.bot.embed_build.convert(ctx, result["response"])
        x["content"] = f"({result['name']}) {x['content'] or ''}"
        await ctx.send(**x)

    @tag.command(name="edit", brief="tag owner")
    async def tag_edit(self, ctx: PretendContext, *, args: str):
        """
        edit a tag
        """

        args = args.split(",", maxsplit=1)

        if len(args) == 1:
            return await ctx.send_warning(
                "No response found. Make sure to use a `,` to split the trigger from the response"
            )

        name = args[0]
        response = args[1].strip()

        check = await self.bot.db.fetchrow(
            """
            SELECT * FROM tags
            WHERE guild_id = $1
            AND name = $2
            """,
            ctx.guild.id,
            name,
        )

        if not check:
            return await ctx.send_warning(f"No tag found for **{name}**")

        if check["author_id"] != ctx.author.id:
            return await ctx.send_warning(f"You are not the **author** of this tag")

        await self.bot.db.execute(
            """
      UPDATE tags
      SET response = $1
      WHERE guild_id = $2
      AND name = $3
      """,
            response,
            ctx.guild.id,
            name,
        )
        await ctx.send_success(f"Updated tag for **{name}**" + f"\n```{response}```")

    @tag.command(name="creator", aliases=["author"])
    async def tag_creator(self, ctx: PretendContext, *, tag: str):
        """
        view the creator of a tag
        """

        check = await self.bot.db.fetchrow(
            """
      SELECT * FROM tags
      WHERE guild_id = $1
      AND name = $2
      """,
            ctx.guild.id,
            tag,
        )

        if not check:
            return await ctx.send_warning(f"No tag found for **{tag}**")

        user = self.bot.get_user(check["author_id"])
        return await ctx.pretend_send(f"The author of this tag is **{user}**")

    @tag.command(name="search")
    async def tag_search(self, ctx: PretendContext, *, query: str):
        """
        search for a tag
        """

        results = await self.bot.db.fetch(
            f"""
      SELECT * FROM tags
      WHERE guild_id = $1
      AND name LIKE '%{query}%'
      """,
            ctx.guild.id,
        )

        if not results:
            return await ctx.send_warning(f"No **tags** found")

        await ctx.paginate(
            [f"**{result['name']}**" for result in results], title=f"Tags like {query}"
        )

    @commands.command(name="color", aliases=["colour"])
    async def color(self, ctx: PretendContext, *, color: Color):
        """
        view info about a color
        """

        embed = discord.Embed(color=color)
        embed.set_author(name=f"Showing hex code: {color}")

        embed.add_field(
            name="RGB Value",
            value=", ".join([str(x) for x in color.to_rgb()]),
            inline=True,
        )
        embed.add_field(name="INT", value=color.value, inline=True)

        embed.set_thumbnail(
            url=(
                "https://place-hold.it/250x219/"
                + str(color).replace("#", "")
                + "?text=%20"
            )
        )

        return await ctx.reply(embed=embed)

    @commands.command(name="transparent", aliases=["tp"])
    @commands.max_concurrency(1, commands.BucketType.channel, wait=True)
    @commands.cooldown(1, 6, commands.BucketType.user)
    async def transparent(self, ctx: PretendContext, url: str = None):
        """
        make an image transparent
        """

        if not url:
            url = await ctx.get_attachment()
            if not url:
                return await ctx.send_help(ctx.command)

            url = url.url

        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        if not re.findall(regex, url):
            return await ctx.send_error("The image provided is not an url")

        try:
            async with ctx.channel.typing(), asyncio.timeout(15):
                return await ctx.reply(
                    file=discord.File(
                        BytesIO(
                            await self.bot.loop.run_in_executor(
                                self.bot.executor,
                                rembg.bg.remove,
                                await self.bot.session.get_bytes(url),
                            )
                        ),
                        "transparent.png",
                    )
                )

        except Exception:
            return await ctx.send_warning(f"Couldn't make the image **transparent**")

    @commands.command(name="image", aliases=["img", "im"])
    @commands.cooldown(1, 1, commands.BucketType.member)
    async def image(self, ctx: PretendContext, *, query: str):
        """
        search for an image
        """

        response = await self.bot.session.post_json(
            f"https://vile.bot/api/browser/images",
            data=query.replace(" ", "%20"),
            params=dict(colors="true"),
        )

        if not response:
            return await ctx.send_warning(f"No results found for **{query}**")

        entries = [
            discord.Embed(
                title=entry.get("title"),
                url=f"https://{entry.get('domain')}",
                color=entry.get("color"),
            )
            .set_image(url=entry.get("url"))
            .set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar
            )
            .set_footer(
                text="Brave Results Searching",
                icon_url="https://upload.wikimedia.org/wikipedia/commons/5/51/Brave_icon_lionface.png",
            )
            for entry in response
        ]

        await ctx.paginator(entries)

    @commands.command(name="inviteinfo", aliases=["ii"], description="get information about an invite", usage="invite code")
    async def inviteinfo(self, ctx, code: str):
        if "/" in code:
            code = code.split("/", -1)[-1].replace(" ", "")

        try:
            invite = await ctx.bot.fetch_invite(url=code, with_counts=True, with_expiration=True)
        except discord.NotFound:
            return await ctx.warning('that was an invalid invite')
        icon= f"[icon]({invite.guild.icon.url})" if invite.guild.icon is not None else "N/A"
        splash=f"[splash]({invite.guild.splash.url})" if invite.guild.splash is not None else "N/A"
        banner=f"[banner]({invite.guild.banner.url})" if invite.guild.banner is not None else "N/A"
        members_total = f"{invite.approximate_member_count:,}"
        members_online_total = f"{invite.approximate_presence_count:,}"
        ratio_string = round(invite.approximate_presence_count / invite.approximate_member_count, 2) * 100
        urls = ""
        embed = discord.Embed(color=self.bot.color, title=f"Invite Code: {code}")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.add_field(name="Channel & Invite", value=f"**Name:** {invite.channel} (`{invite.channel.type}`)\n**ID:** `{invite.channel.id}`\n**Created:** <t:{str(invite.channel.created_at.timestamp()).split('.')[0]}> (<t:{str(invite.channel.created_at.timestamp()).split('.')[0]}:R>)\n**Invite Expiration:** {invite.max_age}\n**Inviter:** {invite.inviter}\n**Temporary:** {invite.temporary}\n**Usage:** {invite.uses}")
        embed.add_field(name="Guild", value=f"**Name:** {invite.guild.name}\n**ID:** `{invite.guild.id}`\n**Created:** <t:{str(invite.guild.created_at.timestamp()).split('.')[0]}> (<t:{str(invite.guild.created_at.timestamp()).split('.')[0]}:R>)\n**Members:** {members_total}\n**Members Online:** {members_online_total}\n**Member Online Ratio:** {ratio_string}\n**Verification Level:** {str(invite.guild.verification_level).title()}")
       # embed.add_field(name="Design", value=f"{icon}\n{splash}\n{banner}")
        if invite.guild.icon is not None:
          embed.set_thumbnail(url=invite.guild.icon.url)

        await ctx.reply(embed=embed)


async def setup(bot: Pretend) -> None:
    return await bot.add_cog(Utility(bot))
