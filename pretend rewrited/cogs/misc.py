import discord
from discord.ext import commands
from pretend.permissions import Permissions
from typing import Optional
from pretend.context import create_pages
from discord import TextChannel, Embed
from pretend.converters import Mod
def is_detention(): 
 async def predicate(ctx: commands.Context): 
  
  check = await ctx.bot.db.fetchrow("SELECT * FROM naughtycorner WHERE guild_id = $1", ctx.guild.id)
  if not check: await ctx.warning("Naughty corner is not configured")
  
  return check is not None 
 return commands.check(predicate)
class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState): 
   
     naughty = await self.bot.db.fetchrow("SELECT * FROM naughtycorner_members WHERE guild_id = $1 AND user_id = $2", member.guild.id, member.id)
   
     if naughty: 
       check = await self.bot.db.fetchrow("SELECT * FROM naughtycorner WHERE guild_id = $1", member.guild.id)
     
       if check:
        channel = member.guild.get_channel(int(check['channel_id']))      
      
        if after.channel.id != channel.id: await member.move_to(channel=channel, reason=f"Moved to the naughty corner")
    @commands.command(description='Pin a message by replying to it', brief='manage messages', usage='[message id]')
    @Permissions.has_permission(manage_messages=True)
    async def pin(self, ctx, message_id: int = None):
        if ctx.message.reference:
            message_id = ctx.message.reference.message_id

        if not message_id:
            await ctx.send_warning("You need to provide a **message ID** or **reply** to the message")
            return

        message = await ctx.channel.fetch_message(message_id)
        await message.pin()
        await ctx.message.add_reaction("👍🏼")

    @commands.command(description='Unpin a message by replying to it', brief='manage messages', usage='[message id]')
    @Permissions.has_permission(manage_messages=True)
    async def unpin(self, ctx, message_id: int = None):
        if ctx.message.reference:
            message_id = ctx.message.reference.message_id

        if not message_id:
            await ctx.send_warning("You need to provide a **message ID** or **reply** to the message")
            return

        message = await ctx.channel.fetch_message(message_id)
        await message.unpin()
        await ctx.message.add_reaction("👍🏼")

    @commands.command(name="channelinfo", aliases=["ci"], usage=" ")
    async def channelinfo(self, ctx, *, channel: Optional[TextChannel] = None):
        channel = channel or ctx.channel
        embed = Embed(
            color=self.bot.color,
            title=f"Channel Info: {channel.name}",
            description=f"Details about the {channel.mention} channel."
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        embed.add_field(name="Channel ID", value=f"{channel.id}", inline=True)
        embed.add_field(name="Type", value=f"{str(channel.type).capitalize()}", inline=True)

        embed.add_field(name="Guild", value=f"{channel.guild.name}", inline=True)
        embed.add_field(name="Category", value=f"{channel.category.name if channel.category else 'None'}", inline=True)

        embed.add_field(name="Topic", value=f"{channel.topic if channel.topic else 'N/A'}", inline=True)
        embed.add_field(
            name="Created At",
            value=f"{discord.utils.format_dt(channel.created_at, style='F')} "
                  f"({discord.utils.format_dt(channel.created_at, style='R')})",
            inline=False
        )

        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar)

        await ctx.send(embed=embed)

    @commands.group(aliases=['detention', 'nc'], invoke_without_command=True)
    async def naughtycorner(self, ctx: commands.Context): 
      await create_pages(ctx)
    
    @naughtycorner.command( aliases=['configure', 'set'], brief="manage server", usage="[voice channel]", name="setup", description="configure naughty corner voice channel")
    @Permissions.has_permission(manage_guild=True)
    async def nc_setup(self, ctx: commands.Context, *, channel: discord.VoiceChannel): 
   
     check = await self.bot.db.fetchrow("SELECT * FROM naughtycorner WHERE guild_id = $1", ctx.guild.id)
     if check: await self.bot.db.execute("UPDATE naughtycorner SET channel_id = $1 WHERE guild_id = $2", channel.id, ctx.guild.id) 
   
     else: await self.bot.db.execute("INSERT INTO naughtycorner VALUES ($1,$2)", ctx.guild.id, channel.id)
     return await ctx.send_success(f"Naughty corner voice channel configured -> {channel.mention}")

    @naughtycorner.command( name="unsetup", brief="manage server", description="disable naughty corner feature in the server") 
    @Permissions.has_permission(manage_guild=True)
    @is_detention()
    async def nc_unsetup(self, ctx: commands.Context): 
   
     await self.bot.db.execute('DELETE FROM naughtycorner WHERE guild_id = $1', ctx.guild.id)
     return await ctx.send_success("Naughty corner is now disabled")
  
    @naughtycorner.command( name="add", brief="timeout members", description="add a member to the naughty corner", usage="[member]")
    @Permissions.has_permission(moderate_members=True)
    @is_detention()
    async def nc_add(self, ctx: commands.Context, *, member: discord.Member): 
   
     if await Mod.check_hieracy(ctx, member): 
    
      check = await self.bot.db.fetchrow("SELECT * FROM naughtycorner_members WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, member.id)
      if check: return await ctx.send_warning("This member is **already** in the naughty corner")
    
      await self.bot.db.execute("INSERT INTO naughtycorner_members VALUES ($1,$2)", ctx.guild.id, member.id)
    
      res = await self.bot.db.fetchrow("SELECT channel_id FROM naughtycorner WHERE guild_id = $1", ctx.guild.id)
      channel = ctx.guild.get_channel(int(res['channel_id']))
    
      await member.move_to(channel=channel, reason=f"Moved to the naughty corner by {ctx.author}")
      return await ctx.send_success(f"Moved **{member}** to {channel.mention if channel else '**Naughty Corner**'}") 
  
    @naughtycorner.command( name="remove", brief="timeout emmbers", description="remove a member from the naughty corner", usage="[member]")
    @Permissions.has_permission(manage_guild=True)
    @is_detention()
    async def nc_remove(self, ctx: commands.Context, *, member: discord.Member): 
   
     if await Mod.check_hieracy(ctx, member): 
      check = await self.bot.db.fetchrow("SELECT * FROM naughtycorner_members WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, member.id)
    
      if not check: return await ctx.warning("this member is **not** in the naughty corner")
    
      await self.bot.db.execute("DELETE FROM naughtycorner_members WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, member.id)
      return await ctx.send_success(f"Removed **{member}** from **naughty corner**") 
   
    @naughtycorner.command(name="members", aliases=['list'], description="returns members from the naughty corner")      
    @is_detention()
    async def nc_list(self, ctx: commands.Context):
      
        results = await self.bot.db.fetch("SELECT user_id FROM naughtycorner_members WHERE guild_id = $1", ctx.guild.id)
        if len(results) == 0: return await ctx.warning("no **whitelisted** members found")
      
        nc_list = [f"<@!{r['user_id']}>" for r in results]
        await ctx.paginator(nc_list, f"members in naughty corner [{len(results)}]")  
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Misc(bot))
