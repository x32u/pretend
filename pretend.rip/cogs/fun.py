import random
import discord
import asyncio
import orjson
import humanize
import datetime
import requests 
import aiohttp

from discord.ext import commands
from discord import (
    Interaction,
    ButtonStyle,
    Embed,
    Member,
    TextChannel,
    User,
    Message,
    AllowedMentions,
    File,
)
from discord.ui import Button, View, button

from discord.ext.commands import (
    BadArgument,
    Cog,
    hybrid_command,
    hybrid_group,
    Author,
    command,
    is_owner,
)

from typing import List
from aiogtts import aiogTTS

from tools.bot import Pretend
from tools.helpers import PretendContext

from tools.converters import AbleToMarry
from tools.helpers import PretendContext
from tools.misc.views import MarryView


class TicTacToeButton(Button["TicTacToe"]):
    def __init__(self, x: int, y: int, player1: Member, player2: Member):
        super().__init__(style=ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y
        self.player1 = player1
        self.player2 = player2

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            if interaction.user != self.player1:
                return await interaction.response.send_message(
                    "You cannot interact with this button", ephemeral=True
                )
            self.style = ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"{self.player1} ?? {self.player2}\n\nIt's **{self.player2.name}**'s turn"
        else:
            if interaction.user != self.player2:
                return await interaction.response.send_message(
                    "You cannot interact with this button", ephemeral=True
                )

            self.style = ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"{self.player1} ?? {self.player2}\n\nIt's **{self.player1.name}'s** turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f"**{self.player1.name}** won!"

                check = await interaction.client.db.fetchrow(
                    """
                SELECT * FROM gamestats
                WHERE user_id = $1
                AND game = $2
                """,
                    self.player1.id,
                    "tictactoe",
                )

                if not check:
                    await interaction.client.db.execute(
                        """
                INSERT INTO gamestats
                VALUES ($1,$2,$3,$4,$5)
                """,
                        self.player1.id,
                        "tictactoe",
                        1,
                        0,
                        1,
                    )
                else:
                    await interaction.client.db.execute(
                        """
                  UPDATE gamestats
                  SET wins = $1,
                  total = $2
                  WHERE user_id = $3
                  AND game = $4
                  """,
                        check["wins"] + 1,
                        check["total"] + 1,
                        self.player1.id,
                        "tictactoe",
                    )

                check2 = await interaction.client.db.fetchrow(
                    """
                SELECT * FROM gamestats 
                WHERE user_id = $1 
                AND game = $2
                """,
                    self.player2.id,
                    "tictactoe",
                )
                if not check2:
                    await interaction.client.db.execute(
                        """
                  INSERT INTO gamestats
                  VALUES ($1,$2,$3,$4,$5)
                  """,
                        self.player2.id,
                        "tictactoe",
                        0,
                        1,
                        1,
                    )
                else:
                    await interaction.client.db.execute(
                        """
                  UPDATE gamestats 
                  SET loses = $1,
                  total = $2
                  WHERE user_id = $3
                  AND game = $4
                  """,
                        check2["loses"] + 1,
                        check2["total"] + 1,
                        self.player2.id,
                        "tictactoe",
                    )

            elif winner == view.O:
                content = f"**{self.player2.name}** won!"

                check = await interaction.client.db.fetchrow(
                    """
                SELECT * FROM gamestats
                WHERE user_id = $1
                AND game = $2
                """,
                    self.player1.id,
                    "tictactoe",
                )
                if not check:
                    await interaction.client.db.execute(
                        """
                INSERT INTO gamestats 
                VALUES ($1,$2,$3,$4,$5)
                """,
                        self.player2.id,
                        "tictactoe",
                        1,
                        0,
                        1,
                    )
                else:
                    await interaction.client.db.execute(
                        """
                  UPDATE gamestats
                  SET wins = $1,
                  total = $2
                  WHERE user_id = $3
                  AND game = $4
                  """,
                        check["wins"] + 1,
                        check["total"] + 1,
                        self.player2.id,
                        "tictactoe",
                    )

                check2 = await interaction.client.db.fetchrow(
                    """
                SELECT * FROM gamestats 
                WHERE user_id = $1
                AND game = $2
                """,
                    self.player1.id,
                    "tictactoe",
                )
                if not check2:
                    await interaction.client.db.execute(
                        """
                  INSERT INTO gamestats
                  VALUES ($1,$2,$3,$4,$5)
                  """,
                        self.player1.id,
                        "tictactoe",
                        0,
                        1,
                        1,
                    )
                else:
                    await interaction.client.db.execute(
                        """
                  UPDATE gamestats 
                  SET loses = $1,
                  total = $2
                  WHERE user_id = $3
                  AND game = $4
                  """,
                        check2["loses"] + 1,
                        check2["total"] + 1,
                        self.player1.id,
                        "tictactoe",
                    )

            else:
                content = "It's a tie!"
                for i in [self.player1.id, self.player2.id]:
                    check = await interaction.client.db.fetchrow(
                        """
                    SELECT * FROM gamestats 
                    WHERE user_id = $1
                    AND game = $2
                    """,
                        i,
                        "tictactoe",
                    )
                    if not check:
                        await interaction.client.db.execute(
                            """
                      INSERT INTO gamestats
                      VALUES ($1,$2,$3,$4,$5)
                      """,
                            i,
                            "tictactoe",
                            0,
                            0,
                            1,
                        )
                    else:
                        await interaction.client.db.execute(
                            """
                      UPDATE gamestats 
                      SET total = $1
                      WHERE user_id = $2
                      AND game = $3
                      """,
                            check["total"] + 1,
                            i,
                            "tictactoe",
                        )

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, player1: Member, player2: Member):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, player1, player2))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class RockPaperScissors(View):
    def __init__(self, ctx: PretendContext):
        self.ctx = ctx
        self.get_emoji = {"rock": "??", "paper": "??", "scissors": "??"}
        self.status = False
        super().__init__(timeout=10)

    async def disable_buttons(self):
        await self.message.edit(view=None)

    async def interaction_check(self, interaction: Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.warn("This is **not** your game")
        return interaction.user.id == self.ctx.author.id

    async def action(self, interaction: Interaction, selection: str):
        botselection = random.choice(["rock", "paper, scissors"])

        def getwinner():
            if botselection == "rock" and selection == "scissors":
                return interaction.client.user.id
            elif botselection == "rock" and selection == "paper":
                return interaction.user.id
            elif botselection == "paper" and selection == "rock":
                return interaction.client.user.id
            elif botselection == "paper" and selection == "scissors":
                return interaction.user.id
            elif botselection == "scissors" and selection == "rock":
                return interaction.user.id
            elif botselection == "scissors" and selection == "paper":
                return interaction.client.user.id
            else:
                return "tie"

        if getwinner() == "tie":
            check = await interaction.client.db.fetchrow(
                """
        SELECT * FROM gamestats 
        WHERE user_id = $1
        AND game = $2
        """,
                interaction.user.id,
                "rockpaperscissors",
            )
            if not check:
                await interaction.client.db.execute(
                    """
          INSERT INTO gamestats 
          VALUES ($1,$2,$3,$4,$5)
          """,
                    interaction.user.id,
                    "rockpaperscissors",
                    0,
                    0,
                    1,
                )
            else:
                await interaction.client.db.execute(
                    """
          UPDATE gamestats 
          SET total = $1
          WHERE user_id = $2
          AND game = $3
          """,
                    check["total"] + 1,
                    interaction.user.id,
                    "rockpaperscissors",
                )

            await interaction.response.edit_message(
                embed=Embed(
                    color=interaction.client.color,
                    title="Tie!",
                    description=f"You both picked {self.get_emoji.get(selection)}",
                )
            )
        elif getwinner() == interaction.user.id:
            check = await interaction.client.db.fetchrow(
                """
        SELECT * FROM gamestats 
        WHERE user_id = $1
        AND game = $2
        """,
                interaction.user.id,
                "rockpaperscissors",
            )
            if not check:
                await interaction.client.db.execute(
                    """
          INSERT INTO gamestats 
          VALUES ($1,$2,$3,$4,$5)
          """,
                    interaction.user.id,
                    "rockpaperscissors",
                    1,
                    0,
                    1,
                )
            else:
                await interaction.client.db.execute(
                    """
          UPDATE gamestats
          SET wins = $1, 
          total = $2
          WHERE user_id = $3
          AND game = $4
          """,
                    check["wins"] + 1,
                    check["total"] + 1,
                    interaction.user.id,
                    "rockpaperscissors",
                )

            await interaction.response.edit_message(
                embed=Embed(
                    color=interaction.client.color,
                    title="You won!",
                    description=f"You picked {self.get_emoji.get(selection)} and the bot picked {self.get_emoji.get(botselection)}",
                )
            )
        else:
            check = await interaction.client.db.fetchrow(
                """
        SELECT * FROM gamestats
        WHERE user_id = $1 
        AND game = $2
        """,
                interaction.user.id,
                "rockpaperscissors",
            )
            if not check:
                await interaction.client.db.execute(
                    """
          INSERT INTO gamestats 
          VALUES ($1,$2,$3,$4,$5)
          """,
                    interaction.user.id,
                    "rockpaperscissors",
                    0,
                    1,
                    1,
                )
            else:
                await interaction.client.db.execute(
                    """
          UPDATE gamestats 
          SET loses = $1, 
          total = $2 
          WHERE user_id = $3 
          AND game = $4
          """,
                    check["loses"] + 1,
                    check["total"] + 1,
                    interaction.user.id,
                    "rockpaperscissors",
                )

            await interaction.response.edit_message(
                embed=Embed(
                    color=interaction.client.color,
                    title="Bot won!",
                    description=f"You picked {self.get_emoji.get(selection)} and the bot picked {self.get_emoji.get(botselection)}",
                )
            )

        await self.disable_buttons()
        self.status = True

    @button(emoji="??")
    async def rock(self, interaction: Interaction, button: Button):
        return await self.action(interaction, "rock")

    @button(emoji="??")
    async def paper(self, interaction: Interaction, button: Button):
        return await self.action(interaction, "paper")

    @button(emoji="??")
    async def scissors(self, interaction: Interaction, button: Button):
        return await self.action(interaction, "scissors")

    async def on_timeout(self):
        if self.status == False:
            await self.disable_buttons()


class BlackTea:
    MatchStart = {}
    lifes = {}

    async def get_string():
        lis = await BlackTea.get_words()
        word = random.choice([l for l in lis if len(l) > 3])
        return word[:3]

    async def get_words():
        with open('./texts/wordlist.txt', 'r') as f:
            data = f.read().splitlines()
        return data


class Fun(Cog):
    def __init__(self, bot: Pretend):
        self.bot = bot
        self.wedding = "??"
        self.marry_color = 0xFF819F
        self.description = "Fun commands"
        self.songkey = "K8thNMhwdBW1ncfVhASKmBHPo0rajjqFD2YYBe_8UFWoIv0nD7hjuLkG2nTO69u0"

    def human_format(self, number: int) -> str:
        """
        Humanize a number, if the case
        """

        if number > 999:
            return humanize.naturalsize(number, False, True)

        return number.__str__()

    async def stats_execute(self, ctx: PretendContext, member: User) -> Message:
        """
        Execute any of the stats commands
        """

        check = await self.bot.db.fetchrow(
            "SELECT * FROM gamestats WHERE game = $1 AND user_id = $2",
            ctx.command.name,
            member.id,
        )

        if not check:
            return await ctx.send_error("There are no stats recorded for this member")

        embed = Embed(
            color=self.bot.color,
            title=f"Stats for {ctx.command.name}",
            description=f"**Wins:** {check['wins']}\n**Loses:** {check['loses']}\n**Matches:** {check['total']}",
        ).set_author(name=member.name, icon_url=member.display_avatar.url)

        return await ctx.reply(embed=embed)

    def shorten(self, value: str, length: int = 32):
        if len(value) > length:
            value = value[: length - 2] + ("..." if len(value) > length else "").strip()
        return value

    @commands.command(description="Make someone a blowjob", help="Make someone a blowjob")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blowjob(self, ctx: commands.Context, *, member: discord.Member):
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(color=self.bot.color, description=f"{self.bot.warning} {ctx.author.mention}: You can't use this NSFW command here.")
            await ctx.reply(embed=embed)
        else:
            url = 'https://api.waifu.pics/nsfw/blowjob'
            resp = requests.get(url)  # Directly using requests.get() instead of session.get()
            js = resp.json()
            embed = discord.Embed(description=f"**{ctx.author.name}** *gives a blowjob to* **{member.name}**", color=self.bot.color)
            embed.set_image(url=js['url'])
            await ctx.reply(embed=embed)

    @hybrid_command()
    async def quran(self, ctx: PretendContext):
        """
        Get a random quran verse
        """

        result = await self.bot.session.get_json(
            "https://api.alquran.cloud/v1/surah/40/en.sahih"
        )
        name = f"{result['data']['name']} ({result['data']['englishName']})"
        number = result["data"]["number"]
        ayah = random.choice(result["data"]["ayahs"])
        numberInSurah = ayah["numberInSurah"]
        text = ayah["text"]

        embed = Embed(
            color=self.bot.color, description=f"**{number}:{numberInSurah}** {text}"
        ).set_author(name=name)

        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def bible(self, ctx: PretendContext):
        """
        Get a random bible verse
        """

        params = {"format": "json", "order": "random"}

        result = await self.bot.session.get_json(
            "https://beta.ourmanna.com/api/v1/get", params=params
        )
        embed = Embed(
            color=self.bot.color, description=result["verse"]["details"]["text"]
        )
        embed.set_author(name=result["verse"]["details"]["reference"])
        await ctx.reply(embed=embed)

    @hybrid_command(
        name="eject",
        help="eject specified user",
        aliases=["imposter"],
    )
    async def eject(self, ctx: PretendContext, user: discord.Member = None):
        user = ctx.author if not user else user

        impostor = ["true", "false"]

        crewmate = [
            "black",
            "blue",
            "brown",
            "cyan",
            "darkgreen",
            "lime",
            "orange",
            "pink",
            "purple",
            "red",
            "white",
            "yellow",
        ]

        await ctx.reply(
            f"https://vacefron.nl/api/ejected?name={user.name}&impostor={random.choice(impostor)}&crewmate={random.choice(crewmate)}"
        )

#    @hybrid_command()
 #   async def blacktea(self, ctx: PretendContext):
  ######

    @hybrid_group(
        invoke_without_command=True,
        description="check a member's stats for a certain game",
    )
    async def stats(self, ctx: PretendContext):
        """
        check a member's stats for a certain game
        """

        await ctx.create_pages()

    @stats.command(name="tictactoe", aliases=["ttt"])
    async def stats_ttt(self, ctx: PretendContext, *, member: User = Author):
        """
        View a member's stats for tictactoe
        """

        await self.stats_execute(ctx, member)

    @stats.command(name="rockpaperscissors", aliases=["rps"])
    async def stats_rps(self, ctx: PretendContext, *, member: User = Author):
        """
        View a member's stats for rockpaperscissors
        """

        await self.stats_execute(ctx, member)

    @command()
    async def pack(self, ctx: PretendContext, *, member: Member):
        """
        Pack a member
        """

        if member == ctx.author:
            return await ctx.reply("Why do you want to pack yourself ://")

        result = await self.bot.session.get_json(
            "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        )
        await ctx.send(
            f"{member.mention} {result['insult']}",
            allowed_mentions=AllowedMentions.none(),
        )

    @hybrid_command(name="8ball")
    async def eightball(self, ctx: PretendContext, *, question: str):
        """
        Ask the 8ball a question
        """

        await ctx.reply(
            f"question: {question}{'?' if not question.endswith('?') else ''}\n{random.choice(['yes', 'no', 'never', 'most likely', 'absolutely', 'absolutely not', 'of course not'])}",
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @hybrid_command()
    async def bird(self, ctx: PretendContext):
        """
        Send a random bird image
        """

        data = await self.bot.session.get_json("https://api.alexflipnote.dev/birb")
        await ctx.reply(
            file=File(fp=await self.bot.getbyte(data["file"]), filename="bird.png")
        )

    @hybrid_command()
    async def dog(self, ctx: PretendContext):
        """
        Send a random dog image
        """

        data = await self.bot.session.get_json("https://random.dog/woof.json")
        await ctx.reply(
            file=File(
                fp=await self.bot.getbyte(data["url"]),
                filename=f"dog{data['url'][-4:]}",
            )
        )

    @hybrid_command()
    async def blacktea(self, ctx: PretendContext):
        """
        idk dawg js blacktea
        """
        try:
            if BlackTea.MatchStart[ctx.guild.id] is True:
                return await ctx.send_warning("someone is already playing blacktea")
        except KeyError:
            pass

        BlackTea.MatchStart[ctx.guild.id] = True
        embed = Embed(description="react with <:tea:1279655472995106816> to join the blacktea game which will begin in **30** seconds", color=self.bot.color)
        embed.add_field(name="goal", value="your goal is to say any word containing the given three letters in 15 seconds")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        mes = await ctx.send(embed=embed)
        await mes.add_reaction("<:tea:1279655472995106816>")
        await asyncio.sleep(30)
        me = await ctx.channel.fetch_message(mes.id)
        players = [user.id async for user in me.reactions[0].users()]
        leaderboard = []
        players.remove(self.bot.user.id)

        if len(players) < 2:
            BlackTea.MatchStart[ctx.guild.id] = False
            return await ctx.send(
                "<:sadJoegbh:1279656112731455564> {}, not enough players joined to start blacktea".format(
                    ctx.author.mention
                ),
                allowed_mentions=discord.AllowedMentions(users=True),
            )

        while len(players) > 1:
            for player in players:
                strin = await BlackTea.get_string()
                await ctx.send(
                    f"<:QuestionMark:1279657909583872102> <@{player}>, type a word containing **{strin.upper()}** in **15 seconds**",
                    allowed_mentions=discord.AllowedMentions(users=True),
                )

                def is_correct(msg):
                    return msg.author.id == player

                try:
                    message = await self.bot.wait_for(
                        "message", timeout=15, check=is_correct
                    )
                except asyncio.TimeoutError:
                    try:
                        BlackTea.lifes[player] = BlackTea.lifes[player] + 1
                        if BlackTea.lifes[player] == 3:
                            await ctx.send(
                                f"<@{player}>, you're eliminated <:laughatthisuser:1279656457532604418>",
                                allowed_mentions=discord.AllowedMentions(
                                    users=True),
                            )
                            BlackTea.lifes[player] = 0
                            players.remove(player)
                            leaderboard.append(player)
                            continue
                    except KeyError:
                        BlackTea.lifes[player] = 0
                    await ctx.send(
                        f"<:laughatthisuser:1279656457532604418> <@{player}>, you didn't reply on time! **{2-BlackTea.lifes[player]}** lifes remaining",
                        allowed_mentions=discord.AllowedMentions(users=True),
                    )
                    continue
                i = 0
                for word in await BlackTea.get_words():
                    if (
                        strin.lower() in message.content.lower()
                        and message.content.lower() == word.lower()
                    ):
                        i += 1
                        pass
                if i == 0:
                    try:
                        BlackTea.lifes[player] = BlackTea.lifes[player] + 1
                        if BlackTea.lifes[player] == 3:
                            await ctx.send(
                                f" <@{player}>, you're eliminated <:laughatthisuser:1279656457532604418>",
                                allowed_mentions=discord.AllowedMentions(
                                    users=True),
                            )
                            BlackTea.lifes[player] = 0
                            players.remove(player)
                            leaderboard.append(player)
                            continue
                    except KeyError:
                        BlackTea.lifes[player] = 0
                    await ctx.send(
                        f"<:laughatthisuser:1279656457532604418> <@{player}>, incorrect word! **{2-BlackTea.lifes[player]}** lifes remaining",
                        allowed_mentions=discord.AllowedMentions(users=True),
                    )
                else:
                    await message.add_reaction("<:thumbsup:1279653766764953694>")
                    i = 0

        leaderboard.append(players[0])
        le = 1
        auto = ""
        for le, leader in enumerate(leaderboard[::-1], start=1):
            auto += f"{'<:CROWN:1279653108670140437>' if le == 1 else f'`{le}`'} **{ctx.guild.get_member(leader) or leader}**\n"
            if le == 10:
                break
            le += 1
        e = discord.Embed(
            color=self.bot.color, title=f"leaderboard for blacktea", description=auto
        ).set_footer(
            text=f"top {'10' if len(leaderboard) > 9 else len(leaderboard)} players"
        )
        await ctx.send(embed=e)
        BlackTea.lifes[players[0]] = 0
        BlackTea.MatchStart[ctx.guild.id] = False

    @hybrid_command()
    async def cat(self, ctx: PretendContext):
        """
        Send a random cat image
        """

        data = (
            await self.bot.session.get_json(
                "https://api.thecatapi.com/v1/images/search"
            )
        )[0]
        await ctx.reply(
            file=File(fp=await self.bot.getbyte(data["url"]), filename="cat.png")
        )

    @hybrid_command()
    async def capybara(self, ctx: PretendContext):
        """
        Send a random capybara image
        """

        data = await self.bot.session.get_json(
            "https://api.capy.lol/v1/capybara?json=true"
        )
        await ctx.reply(
            file=File(
                fp=await self.bot.getbyte(data["data"]["url"]), filename="cat.png"
            )
        )

    @hybrid_command(aliases=["fact", "uf"])
    async def uselessfact(self, ctx: PretendContext):
        """
        Returns an useless fact
        """

        data = (
            await self.bot.session.get_json(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            )
        )["text"]
        await ctx.reply(data)

    @hybrid_command(aliases=["rps"])
    async def rockpaperscisssors(self, ctx: PretendContext):
        """
        Play rockpapaerscissors
        """

        view = RockPaperScissors(ctx)
        embed = Embed(
            color=self.bot.color,
            title="Rock Paper Scissors!",
            description="Click a button to play!",
        )
        view.message = await ctx.reply(embed=embed, view=view)

    @command(name="choose")
    async def choose_cmd(self, ctx: PretendContext, *, choices: str):
        """
        Choose between options
        """

        if len(choices := choices.split(", ")) == 1:
            return await ctx.send_warning(
                f"Not enough **choices**- seperate your choices with a `,`"
            )

        final = random.choice(choices).strip()
        return await ctx.pretend_send(f"I chose `{final}`")

    @command(name="quickpoll", aliases=["poll"])
    async def quickpoll_cmd(self, ctx: PretendContext, *, question: str):
        """
        Create a poll
        """

        message = await ctx.reply(
            embed=Embed(color=self.bot.color, description=question).set_author(
                name=f"{ctx.author} asked"
            )
        )

        for m in ["??", "??"]:
            await message.add_reaction(m)

    @hybrid_command()
    async def ship(self, ctx, member: Member):
        """
        Check the ship rate between you and a member
        """

        return await ctx.reply(
            f"**{ctx.author.name}** ?? **{member.name}** = **{random.randrange(101)}%**"
        )

    @hybrid_command()
    async def advice(self, ctx: PretendContext):
        """
        Get a random advice
        """

        data = orjson.loads(
            await self.bot.session.get_text("https://api.adviceslip.com/advice")
        )
        return await ctx.reply(data["slip"]["advice"])

    @hybrid_command(name="tictactoe", aliases=["ttt"])
    async def tictactoe(self, ctx: PretendContext, *, member: Member):
        """
        Play tictactoe with a member
        """

        if member.id == ctx.author.id:
            return await ctx.send_warning("You cannot play against yourself")

        if member.bot:
            return await ctx.send_warning("You cannot play against a bot")

        view = TicTacToe(ctx.author, member)
        view.message = await ctx.send(
            content=f"{ctx.author} ?? {member}\n\nIt's {ctx.author.name}'s turn",
            view=view,
        )

    @command(aliases=["tts"])
    async def textospeech(self, ctx: PretendContext, *, message: str):
        """
        Convert your message into audio
        """

        await aiogTTS().save(message, "tts.mp3", "en")
        await ctx.reply(file=File(r"tts.mp3"))

    @command()
    async def gay(self, ctx: PretendContext, *, member: Member = Author):
        """
        Gay rate a member
        """
        a = 1
        if member.id == 461914901624127489:
            a = 100
        embed = Embed(
            color=self.bot.color,
            description=f"{member.mention} is **{random.randint(a, 100)}%** gay ??????",
        )
        return await ctx.reply(embed=embed)

    @command()
    async def furry(self, ctx: PretendContext, *, member: Member = Author):
        """
        Furry rate a member
        """
        a = 1
        embed = Embed(
            color=self.bot.color,
            description=f"{member.mention} is **{random.randint(a, 100)}%** a furry ??",
        )
        return await ctx.reply(embed=embed)

    @command(name="dadjoke", aliases=["cringejoke"])
    async def dadjoke(self, ctx: PretendContext):
        """
        Get a random dad joke.
        """
        try:
            joke = await asyncio.wait_for(
                self.bot.session.get_json("https://icanhazdadjoke.com/slack"), timeout=2
            )
        except asyncio.TimeoutError:
            return await ctx.send_warning(
                "Womp Womp! Couldn't get a dad joke at this time."
            )
        return await ctx.pretend_send(f"{joke['attachments'][0]['text']}")

    @command(name="meme")
    async def meme(self, ctx: PretendContext):
        """
        Generate a random meme.
        """
        try:
            meme = await asyncio.wait_for(
                self.bot.session.get_json("https://meme-api.com/gimme"), timeout=4
            )
        except asyncio.TimeoutError:
            return await ctx.send_warning("Error fetching a meme.")
        embed = discord.Embed(color=0x2B2D31)
        embed.set_image(url=meme["url"])
        await ctx.reply(embed=embed)

    @command(name="lick", aliases=["slurp"])
    async def lick(self, ctx: PretendContext, *, member: Member = Author):
        """
        Lick someone!
        """
        if ctx.author.id == member.id:
            return await ctx.send_error("You can't lick yourself!")
        res = ["You slurp that mf.", "Lick Lick!", "Slurp!"]
        embed = Embed(
            color=self.bot.color,
            description=f"You lick {member.nick or member.global_name or member.name}!",
        )
        try:
            lick = await asyncio.wait_for(
                self.bot.session.get_json(
                    "https://api.otakugifs.xyz/gif?reaction=lick&format=gif"
                ),
                timeout=6,
            )
        except asyncio.TimeoutError:
            return await ctx.send_error("There was an error with the API.")
        embed.set_footer(text=random.choice(res))
        embed.set_image(url=lick["url"])
        await ctx.reply(embed=embed)

    @command()
    async def pp(self, ctx: PretendContext, *, member: Member = Author):
        """
        Check someone's pp size
        """
        m = 15
        mn = 1
        if member.id in (461914901624127489, 1174502631696252962, 732610694842810449):
            m = 100
            mn = 20
        embed = Embed(
            color=self.bot.color,
            description=f"{member.nick or member.global_name or member.name}'s penis\n\n8{'=' * random.randint(mn, m)}D",
        )
        await ctx.reply(embed=embed)

    @hybrid_command()
    async def kiss(self, ctx: PretendContext, *, member: Member):
        """
        Kiss a member
        """
        try:
            lol = await asyncio.wait_for(
                self.bot.session.get_json(
                    "https://api.otakugifs.xyz/gif?reaction=kiss&format=gif"
                ),
                timeout=2,
            )
        except asyncio.TimeoutError:
            return await ctx.send_error("There was an error with the API.")
        embed = Embed(
            color=self.bot.color,
            description=f"*Aww how cute!* **{ctx.author.name}** kissed **{member.name}**",
        )
        embed.set_image(url=lol["url"])
        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def pinch(self, ctx: PretendContext, *, member: Member):
        """
        Pinch a member
        """

        response = await self.bot.session.get_json(
            "https://api.otakugifs.xyz/gif?reaction=pinch&format=gif"
        )
        embed = Embed(
            color=self.bot.color,
            description=f"**{ctx.author.name}** pinches **{member.name}**",
        )
        embed.set_image(url=response["url"])

        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def cuddle(self, ctx: PretendContext, *, member: Member):
        """
        Cuddle a member
        """
        try:
            lol = await asyncio.wait_for(
                self.bot.session.get_json(
                    "https://api.otakugifs.xyz/gif?reaction=cuddle&format=gif"
                ),
                timeout=2,
            )
        except asyncio.TimeoutError:
            return await ctx.send_error("There was an error with the API.")
        embed = Embed(
            color=self.bot.color,
            description=f"*Aww how cute!* **{ctx.author.name}** cuddles **{member.name}**",
        ).set_image(url=lol["url"])
        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def hug(self, ctx: PretendContext, *, member: Member):
        """
        Hug a member
        """
        try:
            lol = await asyncio.wait_for(
                self.bot.session.get_json(
                    f"https://api.otakugifs.xyz/gif?reaction=hug&format=gif"
                ),
                timeout=2,
            )
        except asyncio.TimeoutError:
            return await ctx.send_error("There was an error with the API.")
        embed = Embed(
            color=self.bot.color,
            description=f"*Aww how cute!* **{ctx.author.name}** hugged **{member.name}**",
        ).set_image(url=lol["url"])
        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def pat(self, ctx: PretendContext, *, member: Member):
        """
        Pat a member
        """
        try:
            lol = await asyncio.wait_for(
                self.bot.session.get_json(
                    f"https://api.otakugifs.xyz/gif?reaction=pat&format=gif"
                ),
                timeout=2,
            )
        except asyncio.TimeoutError:
            return await ctx.send_error("There was an error with the API.")
        embed = Embed(
            color=self.bot.color,
            description=f"*Aww how cute!* **{ctx.author.name}** pats **{member.name}**",
        ).set_image(url=lol["url"])
        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def slap(self, ctx: PretendContext, *, member: Member):
        """
        Slap a member
        """
        try:
            lol = await asyncio.wait_for(
                self.bot.session.get_json(
                    f"https://api.otakugifs.xyz/gif?reaction=slap&format=gif"
                ),
                timeout=2,
            )
        except asyncio.TimeoutError:
            return await ctx.send_error("There was an error with the API.")
        embed = Embed(
            color=self.bot.color,
            description=f"**{ctx.author.name}** slaps **{member.name}***",
        ).set_image(url=lol["url"])
        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def laugh(self, ctx: PretendContext):
        """
        Start laughing
        """
        try:
            lol = await asyncio.wait_for(
                self.bot.session.get_json(
                    f"https://api.otakugifs.xyz/gif?reaction=laugh&format=gif"
                ),
                timeout=2,
            )
        except asyncio.TimeoutError:
            return await ctx.send_error("There was an error with the API.")
        embed = Embed(
            color=self.bot.color, description=f"**{ctx.author.name}** laughs"
        ).set_image(url=lol["url"])
        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def cry(self, ctx: PretendContext):
        """
        Start crying
        """
        try:
            lol = await asyncio.wait_for(
                self.bot.session.get_json(
                    f"https://api.otakugifs.xyz/gif?reaction=cry&format=gif"
                ),
                timeout=2,
            )
        except asyncio.TimeoutError:
            return await ctx.send_error("There was an error with the API.")

        embed = Embed(
            color=self.bot.color, description=f"**{ctx.author.name}** cries"
        ).set_image(url=lol["url"])
        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def marry(self, ctx: PretendContext, *, member: AbleToMarry):
        """
        Marry a member
        """

        embed = Embed(
            color=self.marry_color,
            description=f"{self.wedding} {ctx.author.mention} wants to marry you. do you accept?",
        )
        view = MarryView(ctx, member)
        view.message = await ctx.reply(content=member.mention, embed=embed, view=view)

    @hybrid_command()
    async def marriage(self, ctx: PretendContext, *, member: User = Author):
        """
        View an user's marriage
        """

        check = await self.bot.db.fetchrow(
            "SELECT * FROM marry WHERE $1 IN (author, soulmate)", member.id
        )
        if check is None:
            return await ctx.send_error(
                f"{'You are' if member == ctx.author else f'{member.mention} is'} not **married**"
            )

        embed = Embed(
            color=self.marry_color,
            description=f"{self.wedding} {f'{member.mention} is' if member != ctx.author else 'You are'} currently married to <@!{check[1] if check[1] != member.id else check[0]}> since **{self.bot.humanize_date(datetime.datetime.fromtimestamp(int(check['time'])))}**",
        )
        return await ctx.reply(embed=embed)

    @hybrid_command()
    async def divorce(self, ctx: PretendContext):
        """
        Divorce from your partner
        """

        check = await self.bot.db.fetchrow(
            "SELECT * FROM marry WHERE $1 IN (author, soulmate)", ctx.author.id
        )
        if check is None:
            return await ctx.send_error("**You** are not **married**")

        async def button1_callback(interaction: Interaction) -> None:
            member = await self.bot.fetch_user(
                check["author"]
                if check["author"] != interaction.user.id
                else check["soulmate"]
            )
            await interaction.client.db.execute(
                "DELETE FROM marry WHERE $1 IN (author, soulmate)", interaction.user.id
            )
            embe = Embed(
                color=interaction.client.color,
                description=f"**{interaction.user.name}** divorced with their partner",
            )

            try:
                await member.send(
                    f"?? It seems like your partner **{interaction.user}** decided to divorce :(. Your relationship with them lasted **{humanize.precisedelta(datetime.datetime.fromtimestamp(int(check['time'])), format=f'%0.0f')}**"
                )
            except:
                pass

            await interaction.response.edit_message(content=None, embed=embe, view=None)

        async def button2_callback(interaction: Interaction) -> None:
            embe = Embed(
                color=interaction.client.color,
                description=f"**{interaction.user.name}** you changed your mind",
            )
            await interaction.response.edit_message(content=None, embed=embe, view=None)

        await ctx.confirmation_send(
            f"{ctx.author.mention} are you sure you want to divorce?",
            button1_callback,
            button2_callback,
        )

    @command(description='get a random TikTok video', aliases=["foryou", "foryoupage"])
    async def fyp(self, ctx: PretendContext):

        async with ctx.typing():
            recommended = await self.bot.session.get_json(url="https://www.tiktok.com/api/recommend/item_list/?WebIdLastTime=1709562791&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F124.0.0.0%20Safari%2F537.36&channel=tiktok_web&clientABVersions=70508271%2C72097972%2C72118536%2C72139452%2C72142433%2C72147654%2C72156694%2C72157773%2C72174908%2C72183344%2C72191581%2C72191933%2C72203590%2C72211002%2C70405643%2C71057832%2C71200802%2C71957976&cookie_enabled=true&count=9&coverFormat=2&device_id=7342516164603889184&device_platform=web_pc&device_type=web_h264&focus_state=true&from_page=fyp&history_len=3&isNonPersonalized=false&is_fullscreen=false&is_page_visible=true&language=en&odinId=7342800074206741537&os=windows&priority_region=&pullType=1&referer=&region=BA&screen_height=1440&screen_width=2560&showAboutThisAd=true&showAds=false&tz_name=Europe%2FLondon&watchLiveLastTime=1713523355360&webcast_language=en&msToken=W3zoVLSFi9M0BsPE6uC63GCdeoVC7hmjRNelZIe-7FP7x-1LRee6WYHYfpWXg3NYPoreJf_dMxfRWTZprVN8UU70_IaHnBMNirtZIRNp2QuR1nBivJgnetgiM-XTh7_KGbNswVs=&X-Bogus=DFSzswVOmtvANegtt2bDG-OckgSu&_signature=_02B4Z6wo00001BozSvQAAIDBhqj5OL8769AaM05AAGCne")
            recommended = recommended['itemList'][0]
            embed = discord.Embed(color=self.bot.color)
            embed.description = f'[{recommended["desc"]}](https://tiktok.com/@{recommended["author"]["uniqueId"]}/video/{recommended["id"]})'

            embed.set_author(
                name="@" + recommended["author"]["uniqueId"],
                icon_url=recommended["author"]["avatarLarger"],
            )
            embed.set_footer(
                text=f"?? {self.human_format(recommended['stats']['diggCount'])} ?? {self.human_format(recommended['stats']['commentCount'])} ?? {self.human_format(recommended['stats']['shareCount'])} ({self.human_format(recommended['stats']['playCount'])} views)"
            )
            
            final = await self.bot.session.get_json("https://tikwm.com/api/", params={"url": f'https://tiktok.com/@{recommended["author"]["uniqueId"]}/video/{recommended["id"]}'})
            await ctx.send(
                embed=embed,
                file=discord.File(fp=await self.bot.getbyte(url=final['data']['play']), filename='pretend.mp4')
            )
            try: await ctx.message.delete()
            except: pass


async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))