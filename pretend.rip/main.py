import discord
import threading
from tools.bot import Pretend
from tools.helpers import PretendContext

bot = Pretend()

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)  # Define Flask app first
CORS(app, resources={r"/*": {"origins": "*"}})  # Apply CORS after app is created

import time
bot_start_time = time.time()

@app.route("/stats", methods=["GET"])
def stats():
    members = sum(guild.member_count for guild in bot.guilds)
    servers = len(bot.guilds)
    avatar = bot.user.display_avatar.url

    shard_count = bot.shard_count  

    shard_data = []
    for shard_id, shard in bot.shards.items():
        uptime_seconds = time.time() - bot_start_time  # Uptime since bot started
        uptime_days = round(uptime_seconds / 86400, 2)  # Convert seconds to days

        shard_data.append({
            "id": shard_id,
            "latency": round(shard.latency * 1000, 2),  # Convert to ms
            "servers": len([g for g in bot.guilds if g.shard_id == shard_id]),
            "uptime_days": uptime_days
        })

    return jsonify({
        "avatar": avatar,
        "members": members,
        "servers": servers,
        "shards": shard_count,
        "shard_data": shard_data
    })



@bot.before_invoke
async def chunk_guild(ctx: PretendContext) -> None:
    if not ctx.guild.chunked:
        await ctx.guild.chunk(cache=True)


@bot.check
async def check_availability(ctx: PretendContext) -> bool:
    return True


@bot.check
async def disabled_command(ctx: PretendContext):
    if await ctx.bot.db.fetchrow(
        """
    SELECT * FROM disablecmd
    WHERE guild_id = $1
    AND cmd = $2
    """,
        ctx.guild.id,
        str(ctx.command),
    ):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send_error(
                f"The command **{str(ctx.command)}** is **disabled** in this server"
            )
            return False
        return True

    global_disabled = await ctx.bot.db.fetchrow(
        """
   SELECT disabled FROM global_disabled_cmds
   WHERE cmd = $1
   """,
        ctx.bot.get_command(str(ctx.command)).name,
    )
    if global_disabled:
        if global_disabled.get("disabled") and ctx.author.id not in ctx.bot.owner_ids:
            await ctx.send_warning(
                "This command is currently disabled by the admin team of pretend, for further information please join the [Pretend Server](https://discord.gg/7jUMQ6YnX5)."
            )
            return False
    return True


@bot.check
async def disabled_module(ctx: PretendContext):
    if ctx.command.cog:
        if await ctx.bot.db.fetchrow(
            """
      SELECT FROM disablemodule
      WHERE guild_id = $1
      AND module = $2
      """,
            ctx.guild.id,
            ctx.command.cog_name,
        ):
            if not ctx.author.guild_permissions.administrator:
                await ctx.send_warning(
                    f"The module **{str(ctx.command.cog_name.lower())}** is **disabled** in this server"
                )
                return False
            else:
                return True
        else:
            return True
    else:
        return True


@bot.check
async def restricted_command(ctx: PretendContext):
    if ctx.author.id == ctx.guild.owner_id:
        return True

    if check := await ctx.bot.db.fetch(
        """
    SELECT * FROM restrictcommand
    WHERE guild_id = $1
    AND command = $2
    """,
        ctx.guild.id,
        ctx.command.qualified_name,
    ):
        for row in check:
            role = ctx.guild.get_role(row["role_id"])
            if not role:
                await ctx.bot.db.execute(
                    """
          DELETE FROM restrictcommand
          WHERE role_id = $1
          """,
                    row["role_id"],
                )

            if not role in ctx.author.roles:
                await ctx.send_warning(f"You cannot use `{ctx.command.qualified_name}`")
                return False
            return True
    return True


@bot.tree.context_menu(name="avatar")
async def avatar_user(interaction: discord.Interaction, member: discord.Member):
    """
    Get a member's avatar
    """

    embed = discord.Embed(
        color=await interaction.client.dominant_color(member.display_avatar.url),
        title=f"{member.name}'s avatar",
        url=member.display_avatar.url,
    )

    embed.set_image(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)


@bot.tree.context_menu(name="banner")
async def banner_user(interaction: discord.Interaction, member: discord.Member):
    """
    Get a member's banner
    """

    member = await interaction.client.fetch_user(member.id)

    if not member.banner:
        return await interaction.warn(f"{member.mention} doesn't have a banner")

    banner = member.banner.url
    embed = discord.Embed(
        color=await interaction.client.dominant_color(banner),
        title=f"{member.name}'s banner",
        url=banner,
    )
    embed.set_image(url=member.banner.url)
    return await interaction.response.send_message(embed=embed)


def run_flask():
    try:
        print("Starting Flask server...")  
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Flask error: {e}")

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("Starting Discord bot...")  # Debug print
    bot.run()  # Start bot after Flask
