import random
import discord 
import aiohttp 
import asyncio
import traceback

from discord import Embed, Interaction, TextChannel
from discord.ui import Select, View, Button 
from tools.helpers import PretendContext
from discord.ext import commands, tasks
from discord.ext.commands import group
from typing import Union
from datetime import datetime
from tools.pfps import PFPS

async def get_genre(category): 
  if category == "male_pfps": return random.choice(PFPS.male)
  elif category == "female_pfps": return random.choice(PFPS.female)
  elif category == "anime_pfps": return random.choice(PFPS.anime)
  elif category == "male_gifs": return random.choice(PFPS.male_gif)
  elif category == "female_gifs": return random.choice(PFPS.female_gif)
  elif category == "anime_gifs": return random.choice(PFPS.anime_gif)
  elif category == "banners": return random.choice(PFPS.banner)

@tasks.loop(seconds=5)
async def autopfp(bot: commands.AutoShardedBot): 
  results = await bot.db.fetch("SELECT * FROM autopfp")
  embed = discord.Embed(color=bot.color, title="Pretend")
  for result in results: 
   print("Pretend AutoPFP Working")
   if result['genre'] == "random": links = await get_genre(random.choice(["anime_pfps", "anime_gifs", "male_pfps", "male_gifs", "female_pfps", "female_gifs"]))
   if result['genre'] == "banner": links = await get_genre("banners")
   else: links = await get_genre(f"{result['genre']}_{result['type']}s")
   embed.set_image(url=links)
   embed.timestamp = datetime.datetime.now()
   embed.set_footer(text="Source: pinterest")
   channel_id = result['channel_id']
   channel = bot.get_channel(channel_id)
   if channel: 
     print("channel found")
     await channel.send(embed=embed)

class Autopfp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @group(invoke_without_command=True) 
    async def autopfp(self, ctx):
       await ctx.create_pages()

    @autopfp.command(help="config", description="Shows variables for the autopost")
    async def genres(self, ctx):
        embed = Embed(
            color=self.bot.color,
            title="Autoimages Related Genres",
            description=f"Here are the **available** genres for both **Autopfp** and **Autogif**. Choose the one that **fits** your needs!"
        )

        embed.add_field(name=f"{self.bot.dash} Autopfp Genres", value=f"**male, female, anime, random, banner**", inline=False)
        embed.add_field(name=f"{self.bot.dash} Autogif Genres", value=f"**male, female, anime, random**", inline=False)

        embed.set_thumbnail(url=self.bot.user.display_avatar)

        await ctx.reply(embed=embed)

    @autopfp.command(name="clear", description="Clear the whole autopfp module", help="config")
    async def autopfp_clear(self, ctx: PretendContext): 
     check = await self.bot.db.fetchrow("SELECT * FROM autopfp WHERE guild_id = $1", ctx.guild.id)
     if not check: return await ctx.send_warning("Autopfp module is **not** configured")
     embed = Embed(color=self.bot.color, description="> Do you truly **wish** to **proceed** with clearing the **AutoPFP** module?")
     yes = Button(emoji=f"<:truepretend:1323118552609460316>")
     no = Button(emoji=f"<:failpretend:1323119435686482001>")

     async def yes_callback(interaction: Interaction): 
       if interaction.user.id != ctx.author.id: return await self.bot.ext.send_warning(interaction, "You are not the **author** of this embed", ephemeral=True)                                      
       await self.bot.db.execute("DELETE FROM autopfp WHERE guild_id = $1", ctx.guild.id)
       return await interaction.response.edit_message(embed=Embed(color=self.bot.color, description=f"> {self.bot.yes} The AutoPFP module has been **successfully** cleared."), view=None)
     
     async def no_callback(interaction: Interaction): 
      if interaction.user.id != ctx.author.id: return await self.bot.ext.send_warning(interaction, "You are not the **author** of this embed", ephemeral=True)                                      
      return await interaction.response.edit_message(embed=Embed(color=self.bot.bot, description=f"> {self.bot.yes} The AutoPFP module hasn't **cleared**"), view=None)

     yes.callback = yes_callback
     no.callback = no_callback
     view = View()
     view.add_item(yes)
     view.add_item(no)
     return await ctx.reply(embed=embed, view=view) 

    @autopfp.command(name="add", description="Add the autopfp module", help="config", usage="[channel] [genre] [type]\nExample: autopfp add #boys male pfp")  
    async def autopfp_add(self, ctx: PretendContext, channel: TextChannel, genre: str, typ: str="none"): 
     try: 
      if genre in ["female", "male", "anime"]: 
        if typ in ["pfp", "gif"]:          
          check = await self.bot.db.fetchrow("SELECT * FROM autopfp WHERE guild_id = $1 AND genre = $2 AND type = $3", ctx.guild.id, genre, typ)                
          if check is not None: return await ctx.send_warning(f"A **dedicated** channel is already **configured** for {genre} {typ}.")
          await self.bot.db.execute("INSERT INTO autopfp VALUES ($1,$2,$3,$4)", ctx.guild.id, channel.id, genre, typ)
          return await ctx.send_success(f"Configured {channel.mention} as {genre} {typ}s")
        else: return await ctx.send_warning("The **specified type** is not **recognized**. Please ensure the value **corresponds** to one of the **following** accepted types: pfp, gif.")
      elif genre in ["random", "banner"]: 
          check = await self.bot.db.fetchrow("SELECT * FROM autopfp WHERE channel_id = $1 AND guild_id = $2 AND genre = $3", channel.id, ctx.guild.id, genre) 
          if check is not None: return await ctx.send_warning(f"A **dedicated** channel is already **configured** for {genre}")
          await self.bot.db.execute("INSERT INTO autopfp VALUES ($1,$2,$3,$4)", ctx.guild.id, channel.id, genre, typ)
          return await ctx.send_success(f"Configured {channel.mention} as {genre} pictures")      
      else: return await ctx.send_error("The **provided** genre is invalid. Accepted values are: male, female, anime, banner, random.")
     except: traceback.print_exc()

    @autopfp.command(name="remove", description="Remove the autopfp module", help="config", usage="[genre] [type]\nExample: autopfp remove male gif")
    async def autopfp_remove(self, ctx: PretendContext, genre: str, typ: str="none"):
       try:  
        check = await self.bot.db.fetchrow("SELECT * FROM autopfp WHERE guild_id = $1 AND genre = $2 AND type = $3", ctx.guild.id, genre, typ)                
        if check is None: return await ctx.send_warning(f"No autopfp channel found for **{genre} {typ if typ != 'none' else ''}**")
        await self.bot.db.execute("DELETE FROM autopfp WHERE guild_id = $1 AND genre = $2 AND type = $3", ctx.guild.id, genre, typ)                
        await ctx.send_success(f"Removed **{genre} {typ if typ != 'none' else ''}** posting")
       except: traceback.print_exc() 

async def setup(bot) -> None: 
    return await bot.add_cog(Autopfp(bot))