import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx):
        await ctx.guild.leave()
        await ctx.message.add_reaction("👍")

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        await ctx.message.add_reaction("⌛")
        await self.bot.tree.sync()
        await ctx.message.clear_reactions()
        return await ctx.message.add_reaction("✅")

async def setup(bot: commands.Bot):
    await bot.add_cog(Owner(bot))
