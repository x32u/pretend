import datetime
import google.generativeai as genai
#from PretendAPI import API

from tools.bot import Pretend
from tools.converters import NoStaff
from tools.helpers import PretendContext
from tools.validators import ValidReskinName
from tools.predicates import has_perks

from discord import User, utils, Embed, Member, AllowedMentions, Interaction
from discord.ext import commands
from discord.ext.commands import (
    Cog,
    command,
    group,
    has_guild_permissions,
    bot_has_guild_permissions,
    Author,
    cooldown,
    max_concurrency,
    hybrid_command,
)



class Donor(Cog):
    def __init__(self, bot: Pretend):
        self.bot = bot
        self.description = "Premium commands"

        genai.configure(api_key="API_KEY")
        self.model = genai.GenerativeModel("gemini-pro")

    def shorten(self, value: str, length: int = 32):
        if len(value) > length:
            value = value[: length - 2] + ("..." if len(value) > length else "").strip()
        return value

    @Cog.listener()
    async def on_user_update(self, before: User, after: User):
        if before.discriminator == "0":
            if before.name != after.name:
                if not self.bot.cache.get("pomelo"):
                    await self.bot.cache.set(
                        "pomelo",
                        [
                            {
                                "username": before.name,
                                "time": utils.format_dt(
                                    datetime.datetime.now(), style="R"
                                ),
                            }
                        ],
                    )
                else:
                    lol = self.bot.cache.get("pomelo")
                    lol.append(
                        {
                            "username": before.name,
                            "time": utils.format_dt(datetime.datetime.now(), style="R"),
                        }
                    )
                    await self.bot.cache.set("pomelo", lol)

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        if str(before.nick) != str(after.nick):
            if nickname := await self.bot.db.fetchval(
                "SELECT nickname FROM force_nick WHERE guild_id = $1 AND user_id = $2",
                before.guild.id,
                before.id,
            ):
                if after.nick != nickname:
                    await after.edit(
                        nick=nickname, reason="Force nickname applied to this member"
                    )

    @command(aliases=["pomelo", "handles"], brief="donor")
    @has_perks()
    async def lookup(self, ctx: PretendContext):
        """get the most recent handles"""
        if not self.bot.cache.get("pomelo"):
            return await ctx.send_error("There is nothing to see here")
        pomelo = self.bot.cache.get("pomelo")
        return await ctx.paginate(
            [f"{m['username']} - {m['time']}" for m in pomelo[::-1]],
            f"Pomelo Usernames ({len(pomelo)})",
        )

    @command(aliases=["sp"], brief="donor")
    @has_perks()
    async def selfpurge(self, ctx: PretendContext, amount: int = 100):
        """delete your own messages"""
        await ctx.channel.purge(
            limit=amount,
            check=lambda m: m.author.id == ctx.author.id and not m.pinned,
            bulk=True,
        )

    @command(
        brief="manage nicknames & donor",
        aliases=["forcenick", "fn"],
    )
    @has_perks()
    @has_guild_permissions(manage_nicknames=True)
    @bot_has_guild_permissions(manage_nicknames=True)
    async def forcenickname(
        self, ctx: PretendContext, member: NoStaff, *, nickname: str = None
    ):
        """lock a nickname to a member"""
        if not nickname:
            if await self.bot.db.fetchrow(
                "SELECT * FROM force_nick WHERE guild_id = $1 AND user_id = $2",
                ctx.guild.id,
                member.id,
            ):
                await self.bot.db.execute(
                    "DELETE FROM force_nick WHERE guild_id = $1 AND user_id = $2",
                    ctx.guild.id,
                    member.id,
                )
                await member.edit(
                    nick=None, reason="Removed the force nickname from this member"
                )
                return await ctx.send_success("Removed the nickname from this member")
            else:
                return await ctx.send_help(ctx.command)
        else:
            if await self.bot.db.fetchrow(
                "SELECT * FROM force_nick WHERE guild_id = $1 AND user_id = $2",
                ctx.guild.id,
                member.id,
            ):
                await self.bot.db.execute(
                    "UPDATE force_nick SET nickname = $1 WHERE guild_id = $2 AND user_id = $3",
                    nickname,
                    ctx.guild.id,
                    member.id,
                )
                await member.edit(
                    nick=nickname, reason="Force nickname applied to this member"
                )
            else:
                await member.edit(
                    nick=nickname, reason="Force nickname applied to this member"
                )
                await self.bot.db.execute(
                    "INSERT INTO force_nick VALUES ($1,$2,$3)",
                    ctx.guild.id,
                    member.id,
                    nickname,
                )
            await ctx.send_success(
                f"Force nicknamed {member.mention} to **{nickname}**"
            )

    @commands.group(invoke_without_command=True, name="reskin", description="customize evicts output embeds")    
    @has_perks()
    async def reskin(self, ctx: PretendContext):
        return await ctx.create_pages()
  
    @reskin.command(name="enable", description="customize evicts output embeds", aliases=['on'], brief="donor")
    @has_perks() 
    async def reskin_enable(self, ctx: PretendContext):
    
        reskin = await self.bot.db.fetchrow("SELECT * FROM reskin WHERE user_id = $1 AND toggled = $2", ctx.author.id, False)
    
        if reskin == None or reskin['toggled'] == False:   
      
            if not await self.bot.db.fetchrow("SELECT * FROM reskin WHERE user_id = $1", ctx.author.id):
                await self.bot.db.execute("INSERT INTO reskin (user_id, toggled, name, avatar) VALUES ($1, $2, $3, $4)", ctx.author.id, True, ctx.author.name, ctx.author.avatar.url)
      
            else:   
                await self.bot.db.execute("UPDATE reskin SET toggled = $1 WHERE user_id = $2", True, ctx.author.id)
      
                return await ctx.send_success("**Reskin** has been **enabled**.")
      
        return await ctx.send_warning("**Reskin** is already **enabled**.")
  
    @reskin.command(name="disable", description="disable the customization output messages", aliases=['off'], brief="donor")
    @has_perks()
    async def reskin_disable(self, ctx: PretendContext):
        reskin = await self.bot.db.fetchrow("SELECT * FROM reskin WHERE user_id = $1 AND toggled = $2", ctx.author.id, True)
    
        if reskin != None and reskin['toggled'] == True:   
      
            await self.bot.db.execute("UPDATE reskin SET toggled = $1 WHERE user_id = $2", False, ctx.author.id)
        return await ctx.send_success("**Reskin** has been **disabled**.")
    
        await self.bot.db.execute("UPDATE reskin SET toggled = $1 WHERE user_id = $2", False, ctx.author.id)
        return await ctx.send_warning("**Reskin** is already **disabled**.")
  
    @reskin.command(name="name", description="change the name used on evicts output embeds", brief="donor")
    @has_perks()
    async def reskin_name(self, ctx: PretendContext, *, name: str=None):
    
        reskin = await self.bot.db.fetchrow("SELECT * FROM reskin WHERE user_id = $1", ctx.author.id)
    
        if not reskin:
            await self.bot.db.execute("INSERT INTO reskin (user_id, toggled, name, avatar) VALUES ($1, $2, $3, $4)", ctx.author.id, True, name, ctx.author.avatar.url)
    
        else:
            await self.bot.db.execute("UPDATE reskin SET name = $1 WHERE user_id = $2", name, ctx.author.id)
      
        if name == None or name.lower() == "none":
            return await ctx.send_success(f"I have set your **reskin** name to `{ctx.author.name}`.")

        return await ctx.send_success(f"I have set **reskin** name to `{name}`.")

    @reskin.command(name="avatar", description="change the icon used on evicts output embeds", aliases=['av'], brief="donor")
    @has_perks()
    async def reskin_avatar(self, ctx: PretendContext, url: str = None):
    
        if url == None and len(ctx.message.attachments) == 0:
            return await ctx.send_warning("you **need** to provide an avatar, either as a **file** or **url**")

        if url == None and len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url

        reskin = await self.bot.db.fetchrow("SELECT * FROM reskin WHERE user_id = $1", ctx.author.id)
    
        if not reskin:
            await self.bot.db.execute("INSERT INTO reskin (user_id, toggled, name, avatar) VALUES ($1, $2, $3, $4)", ctx.author.id, True, ctx.author.name, url)
    
        else:
            await self.bot.db.execute("UPDATE reskin SET avatar = $1 WHERE user_id = $2", url, ctx.author.id)
      
        return await ctx.send_success(f"I have set your **reskin** avatar to [**image**]({url}).")

    @commands.command(description="Talk to AI", name="chatgpt", aliases=["chat", "gpt", "ask"], help="donor")
    @has_perks()
    async def chatgpt(self, ctx, *, query: str):
        async with ctx.channel.typing():
            genai.configure(api_key="AIzaSyB61KW2GlkfjAmc7GNkFCtnj8zkzhgtHsk")
            model = genai.GenerativeModel("gemini-pro")

            response = model.generate_content(query)
            await ctx.send(response.text, allowed_mentions=AllowedMentions.none())


async def setup(bot: Pretend) -> None:
    await bot.add_cog(Donor(bot))
