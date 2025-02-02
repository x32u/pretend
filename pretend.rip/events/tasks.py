from discord.ext import tasks, commands
import discord, asyncio, random, datetime
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
  embed = discord.Embed(color=bot.color, title="")
  for result in results: 
   print("Pretend AutoPFP Working")
   if result['genre'] == "random": links = await get_genre(random.choice(["anime_pfps", "anime_gifs", "male_pfps", "male_gifs", "female_pfps", "female_gifs"]))
   if result['genre'] == "banner": links = await get_genre("banners")
   else: links = await get_genre(f"{result['genre']}_{result['type']}s")
   embed.set_image(url=links)
   embed.timestamp = datetime.datetime.now()
   embed.set_footer(text="you can stop autopfp by typing the command autopfp remove")
   channel_id = result['channel_id']
   channel = bot.get_channel(channel_id)
   if channel: 
     print("channel found")
     await channel.send(embed=embed)
    

class Tasks(commands.Cog): 
    def __init__(self, bot: commands.AutoShardedBot): 
      self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self): 
      await self.bot.wait_until_ready()  
      autopfp.start(self.bot)   
      

async def setup(bot: commands.AutoShardedBot) -> None:
    await bot.add_cog(Tasks(bot))                 