import re
import emoji
import string
import matplotlib
import discord
from discord.ext.commands import (
    Converter,
    BadArgument,
    MemberConverter,
    RoleConverter,
    BotMissingPermissions,
)

from pydantic import BaseModel


class ColorSchema(BaseModel):
    """
    Schema for colors
    """

    hex: str
    value: int


class AnyEmoji(Converter):
    async def convert(self, ctx, argument: str):
        if emoji.is_emoji(argument):
            return argument

        emojis = re.findall(
            r"<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>",
            argument,
        )

        if len(emojis) == 0:
            raise BadArgument(f"**{argument}** is **not** an emoji")

        emoj = emojis[0]
        format = ".gif" if emoj[0] == "a" else ".png"
        return await ctx.bot.session.get_bytes(
            f"https://cdn.discordapp.com/emojis/{emoj[2]}{format}"
        )


class EligibleVolume(Converter):
    async def convert(self, ctx, argument: str):
        try:
            volume = int(argument)
        except ValueError:
            raise BadArgument("This is **not** a number")

        if volume < 0 or volume > 500:
            raise BadArgument("Volume has to be between **0** and **500**")

        return volume


class HexColor(Converter):
    async def convert(self, ctx, argument: str) -> ColorSchema:
        if argument in ["pfp", "avatar"]:
            dominant = await ctx.bot.dominant_color(ctx.author.display_avatar)
            payload = {"hex": hex(dominant).replace("0x", "#"), "value": dominant}
        else:
            color = matplotlib.colors.cnames.get(argument)

            if not color:
                color = argument.replace("#", "")
                digits = set(string.hexdigits)
                if not all(c in digits for c in color):
                    raise BadArgument("This is not a hex code")

            color = color.replace("#", "")
            payload = {"hex": f"#{color}", "value": int(color, 16)}

        return ColorSchema(**payload)


class AbleToMarry(MemberConverter):
    async def convert(self, ctx, argument: str):
        try:
            member = await super().convert(ctx, argument)
        except BadArgument:
            raise BadArgument("This is **not** a member")

        if member == ctx.author:
            raise BadArgument("You cannot marry yourself")

        if member.bot:
            raise BadArgument("You cannot marry a bot")

        if await ctx.bot.db.fetchrow(
            "SELECT * FROM marry WHERE $1 IN (author, soulmate)", member.id
        ):
            raise BadArgument(f"**{member}** is already married")

        if await ctx.bot.db.fetchrow(
            "SELECT * FROM marry WHERE $1 IN (author, soulmate)", ctx.author.id
        ):
            raise BadArgument(
                "You are already **married**. Are you trying to cheat?? 🤨"
            )

        return member


class NoStaff(MemberConverter):
    async def convert(self, ctx, argument: str):
        try:
            member = await super().convert(ctx, argument)
        except BadArgument:
            raise BadArgument("Member not found")

        if ctx.guild.me.top_role.position <= member.top_role.position:
            raise BadArgument("The bot cannot manage this member")

        if ctx.command.qualified_name in ["ban", "kick", "softban", "strip"]:
            if ctx.author.id == member.id:
                if ctx.author.id == ctx.guild.owner_id:
                    raise BadArgument("You cannot execute this command on yourself")
        else:
            if ctx.author.id == member.id:
                return member

        if ctx.author.id == ctx.guild.owner_id:
            return member
        if member.id == ctx.guild.owner_id:
            raise BadArgument("You cannot punish the server owner")
        if ctx.author.top_role.position <= member.top_role.position:
            raise BadArgument(f"You cannot manage **{member.mention}**")

        return member


class LevelMember(MemberConverter):
    async def convert(self, ctx, argument: str):
        try:
            member = await super().convert(ctx, argument)
        except BadArgument:
            raise BadArgument("Member not found")

        if ctx.author.id == member.id:
            return member

        if member.id == ctx.guild.owner_id:
            raise BadArgument("You cannot change the level stats of the server owner")
        if ctx.author.id == ctx.guild.owner_id:
            return member
        if ctx.author.top_role.position <= member.top_role.position:
            raise BadArgument(f"You cannot manage **{member.mention}**")

        return member


class CounterMessage(Converter):
    async def convert(self, ctx, argument: str):
        if not "{target}" in argument:
            raise BadArgument("{target} variable is **missing** from the channel name")

        return argument


class ChannelType(Converter):
    async def convert(self, ctx, argument: str):
        if not argument in ["voice", "stage", "text", "category"]:
            raise BadArgument(f"**{argument}** is not a **valid** channel type")

        return argument


class CounterType(Converter):
    async def convert(self, ctx, argument: str):
        if not argument in ["members", "voice", "boosters", "humans", "bots"]:
            raise BadArgument(f"**{argument}** is not an **available** counter")

        return argument


class NewRoleConverter(RoleConverter):
    async def convert(self, ctx, argument: str):
        try:
            role = await super().convert(ctx, argument)
        except BadArgument:
            role = ctx.find_role(argument)
            if not role:
                raise BadArgument("Role not found")

        if not ctx.guild.me.guild_permissions.manage_roles:
            raise BotMissingPermissions(
                "The bot doesn't have proper permissions to execute this command"
            )

        if role.position >= ctx.guild.me.top_role.position:
            raise BadArgument("This role is over my highest role")

        if not role.is_assignable():
            raise BadArgument("This role cannot be added to anyone by me")

        if ctx.author.id == ctx.guild.owner_id:
            return role

        if role.position >= ctx.author.top_role.position:
            raise BadArgument("You cannot manage this role")

        return role


class EligibleEconomyMember(MemberConverter):
    async def convert(self, ctx, argument: str):
        try:
            member = await super().convert(ctx, argument)
        except BadArgument:
            raise BadArgument("Member **not** found")

        if member.id == ctx.author.id:
            raise BadArgument("You cannot transfer to yourself")

        check = await ctx.bot.db.fetchrow(
            "SELECT * FROM economy WHERE user_id = $1", member.id
        )

        if not check:
            raise BadArgument("This member does not have an economy account created")

        return member


class Punishment(Converter):
    async def convert(self, ctx, argument: str):
        if not argument in ["ban", "kick", "strip"]:
            raise BadArgument(
                f"**{argument}** is **not** a valid punishment\nThe valid ones are: ban, kick and strip"
            )

        return argument

class Perms: 

  def server_owner(): 
   async def predicate(ctx): 
    if ctx.author.id != ctx.guild.owner_id: 
      await ctx.send_warning( f"This command can be used only by **{ctx.guild.owner}**") 
      return False 
    return True   
   return commands.check(predicate)
   
  def get_perms(perm: str=None):
   async def predicate(ctx):  
    if perm is None: return True 
    if ctx.guild.owner == ctx.author: return True
    if ctx.author.guild_permissions.administrator: return True
    for r in ctx.author.roles:
     if perm in [str(p[0]) for p in r.permissions if p[1] is True]: return True 
     check = await ctx.bot.db.fetchrow("SELECT permissions FROM fake_permissions WHERE role_id = $1 and guild_id = $2", r.id, r.guild.id)
     if check is None: continue 
     permissions = json.loads(check[0])
     if perm in permissions or "administrator" in permissions: return True
    raise commands.MissingPermissions([perm])
   return commands.check(predicate)  

  async def has_perms(ctx, perm: str=None): 
    if perm is None: return True 
    if ctx.guild.owner == ctx.author: return True
    if ctx.author.guild_permissions.administrator: return True
    for r in ctx.author.roles:
     if perm in [str(p[0]) for p in r.permissions if p[1] is True]: return True 
     check = await ctx.bot.db.fetchrow("SELECT permissions FROM fake_permissions WHERE role_id = $1 and guild_id = $2", r.id, r.guild.id)
     if check is None: continue 
     permissions = json.loads(check[0])
     if perm in permissions or "administrator" in permissions: return True
    return False   

class Mod: 

  def is_mod_configured(): 
   async def predicate(ctx): 
    check = await ctx.bot.db.fetchrow("SELECT * FROM mod WHERE guild_id = $1", ctx.guild.id)
    if not check: 
     await ctx.warning( f"Moderation isn't **enabled** in this server. Enable it using `{ctx.clean_prefix}setmod` command")
     return False
    return True
   return commands.check(predicate)

  async def check_role_position(ctx, role: discord.Role) -> bool: 
   if (role.position >= ctx.author.top_role.position and ctx.author.id != ctx.guild.owner_id) or not role.is_assignable(): 
    await ctx.warning( "I cannot manage this role for you")
    return False 
   return True

  async def check_hieracy(ctx, member: discord.Member) -> bool: 
   if member.id == ctx.bot.user.id: 
    if ctx.command.name != "nickname":
     await ctx.reply("leave me alone <:mmangry:1081633006923546684>") 
     return False
   if (ctx.author.top_role.position <= member.top_role.position and ctx.guild.owner_id != ctx.author.id) or ctx.guild.me.top_role <= member.top_role or (member.id == ctx.guild.owner_id and ctx.author.id != member.id): 
    await ctx.warning( "You can't do this action on **{}**".format(member))
    return False  
   return True 