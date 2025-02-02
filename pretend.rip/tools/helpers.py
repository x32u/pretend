import sys
import json
import asyncio
import datetime
import humanize
import discord

from discord.ext.commands.cog import Cog
from discord.interactions import Interaction

from typing import Mapping, Coroutine, List, Any, Callable, Optional, Union, Dict
from discord_paginator import Paginator

from .misc.views import ConfirmView

from discord.ext.commands import (
    Context,
    BadArgument,
    HelpCommand as Help,
    Command,
    MissingPermissions,
    check,
    Group,
    AutoShardedBot as AB,
    FlagConverter,
)

from discord import (
    Role,
    ButtonStyle,
    Message,
    Embed,
    StickerItem,
    Interaction,
    User,
    Member,
    Attachment,
    WebhookMessage,
    TextChannel,
    Guild,
    utils,
    Thread,
    SelectOption
)

from discord.ui import Select, View
from typing import Sequence


def guild_perms(**perms: bool) -> Any:

    async def predicate(ctx: PretendContext):
        author_permissions = [p[0] for p in ctx.author.guild_permissions if p[1]]
        if not any(p in author_permissions for p in perms):
            roles = ", ".join(list(map(lambda r: str(r.id), ctx.author.roles)))
            results = await ctx.bot.db.fetch(
                f"SELECT perms FROM fake_perms WHERE guild_id = $1 AND role_id IN ({roles})",
                ctx.guild.id,
            )
            for result in results:
                fake_perms = json.loads(result[0])

                if "administrator" in fake_perms:
                    return True

                if any(p in fake_perms for p in perms):
                    return True
            raise MissingPermissions([p for p in perms])
        return True

    return check(predicate)


async def identify(self):
    payload = {
        "op": self.IDENTIFY,
        "d": {
            "token": self.token,
            "properties": {
                "$os": sys.platform,
                "$browser": "Discord iOS",
                "$device": "Discord iOS",
                "$referrer": "",
                "$referring_domain": "",
            },
            "compress": True,
            "large_threshold": 250,
            "v": 3,
        },
    }

    if self.shard_id is not None and self.shard_count is not None:
        payload["d"]["shard"] = [self.shard_id, self.shard_count]

    state = self._connection
    if state._activity is not None or state._status is not None:
        payload["d"]["presence"] = {
            "status": state._status,
            "game": state._activity,
            "since": 0,
            "afk": False,
        }

    if state._intents is not None:
        payload["d"]["intents"] = state._intents.value

    await self.call_hooks(
        "before_identify", self.shard_id, initial=self._initial_identify
    )
    await self.send_as_json(payload)


class AntinukeMeasures:
    def __init__(self: "AntinukeMeasures", bot: AB):
        self.bot = bot
        self.thresholds = {}

    def get_bot_perms(self, guild: Guild) -> bool:
        """check if the bot can actually punish members"""
        return all(
            [
                guild.me.guild_permissions.ban_members,
                guild.me.guild_permissions.kick_members,
                guild.me.guild_permissions.manage_roles,
            ]
        )

    def check_hieracy(self: "AntinukeMeasures", member: Member, bot: Member) -> bool:
        """
        check if the bot has access to punish this member
        """

        if member.top_role:
            if bot.top_role:
                if member.top_role >= bot.top_role:
                    return False
                else:
                    return True
            else:
                return False
        else:
            if bot.top_role:
                return True
            else:
                return False

    async def is_module(self: "AntinukeMeasures", module: str, guild: Guild) -> bool:
        """
        check if the specific module is available in the guild
        """

        return (
            await self.bot.db.fetchrow(
                """
      SELECT * FROM antinuke_modules
      WHERE module = $1
      AND guild_id = $2
      """,
                module,
                guild.id,
            )
            is not None
        )

    async def is_whitelisted(self: "AntinukeMeasures", member: Member) -> bool:
        """
        check if the specific member is whitelisted in any way
        """

        check = await self.bot.db.fetchrow(
            """
      SELECT owner_id, admins, whitelisted FROM antinuke
      WHERE guild_id = $1
      """,
            member.guild.id,
        )

        if member.id == check["owner_id"]:
            return True

        if check["whitelisted"]:
            if member.id in json.loads(check["whitelisted"]):
                return True

        if check["admins"]:
            if member.id in json.loads(check["admins"]):
                return True

        return False

    async def decide_punishment(
        self: "AntinukeMeasures", module: str, member: Member, reason: str
    ):
        """
        decide the punishment the member is getting
        """

        if member.bot:
            return member.kick(reason=reason)

        punishment = await self.bot.db.fetchval(
            """
      SELECT punishment FROM antinuke_modules
      WHERE guild_id = $1
      AND module = $2
      """,
            member.guild.id,
            module,
        )

        if punishment == "ban":
            return member.ban(reason=reason)

        elif punishment == "kick":
            return member.kick(reason=reason)

        else:
            return member.edit(
                roles=[r for r in member.roles if not r.is_assignable()], reason=reason
            )

    async def check_threshold(
        self: "AntinukeMeasures", module: str, member: Member
    ) -> bool:
        """
        check if a member exceeded the threshold of the specific module
        """

        check = await self.bot.db.fetchval(
            """
      SELECT threshold FROM antinuke_modules 
      WHERE module = $1
      AND guild_id = $2
      """,
            module,
            member.guild.id,
        )

        if check == 0:
            return True

        payload = self.thresholds
        if payload:
            if not payload.get(module):
                payload[module] = {}

            if not payload[module].get(member.guild.id):
                payload[module][member.guild.id] = {}

            if not payload[module][member.guild.id].get(member.id):
                payload[module][member.guild.id][member.id] = [datetime.datetime.now()]
            else:
                payload[module][member.guild.id][member.id].append(
                    datetime.datetime.now()
                )

        else:
            payload = {
                module: {member.guild.id: {member.id: [datetime.datetime.now()]}}
            }

        to_remove = [
            d
            for d in payload[module][member.guild.id][member.id]
            if (datetime.datetime.now() - d).total_seconds() > 60
        ]

        for r in to_remove:
            payload[module][member.guild.id][member.id].remove(r)

        self.thresholds = payload

        if check < len(payload[module][member.guild.id][member.id]):
            return True

        return False

    async def take_action(
        self: "AntinukeMeasures",
        action: str,
        user: Member,
        tasks: list,
        action_time: datetime.datetime,
        owner_id: int,
        channel: TextChannel = None,
    ):
        """
        the action against the nuke attempt
        """

        await asyncio.gather(*tasks)
        time = humanize.precisedelta(action_time)
        embed = (
            Embed(
                color=self.bot.color,
                title="User punished",
                description=f"**{self.bot.user.name}** took **{time}** to take action",
            )
            .set_author(name=user.guild.name, icon_url=user.guild.icon)
            .add_field(name="Server", value=user.guild.name, inline=True)
            .add_field(name="User", value=str(user), inline=False)
            .add_field(name="Reason", value=action, inline=False)
        )

        if channel:
            return await channel.send(embed=embed)

        owner = self.bot.get_user(owner_id)
        try:
            await owner.send(embed=embed)
        except:
            pass


class Cache:
    def __init__(self):
        self.cache_inventory = {}

    def __repr__(self) -> str:
        return str(self.cache_inventory)

    async def do_expiration(self, key: str, expiration: int) -> None:
        await asyncio.sleep(expiration)
        self.cache_inventory.pop(key)

    def get(self, key: str) -> Any:
        """Get the object that is associated with the given key"""
        return self.cache_inventory.get(key)

    async def set(self, key: str, object: Any, expiration: Optional[int] = None) -> Any:
        """Set any object associatng with the given key"""
        self.cache_inventory[key] = object
        if expiration:
            asyncio.ensure_future(self.do_expiration(key, expiration))
        return object

    def remove(self, key: str) -> None:
        """An alias for delete method"""
        return self.delete(key)

    def delete(self, key: str) -> None:
        """Delete a key from the cache"""
        if self.get(key):
            del self.cache_inventory[key]
            return None


class CustomInteraction(Interaction):
    def __init__(self):
        super().__init__()
    
        self.ec_emoji = "🏦"
        self.ec_color = 0xD3D3D3
        
        self.w_color = 0xEFBC1B
        self.n_color = 0xFC341B
        self.y_color = 0x48DB01
        self.c_color = 0x2b2d31

        self.w = "<:warn:1251929429165477948>"
        self.n = "<:deny:1251929424777969797>"
        self.y = "<:check:1251929419795398708>"

    async def error(self, message: str, ephemeral: bool = False) -> None:
        return await self.response.send_message(
            embed=Embed(
                color=0xFC341B,
                description=f"{self.client.no} {self.user.mention}: {message}",
            ),
            ephemeral=ephemeral,
        )

    async def warn(self, message: str, ephemeral: bool = False) -> None:
        return await self.response.send_message(
            embed=Embed(
                color=0xEFBC1B,
                description=f"{self.client.warning} {self.user.mention}: {message}",
            ),
            ephemeral=ephemeral,
        )

    async def approve(self, message: str, ephemeral: bool = False) -> None:
        return await self.response.send_message(
            embed=Embed(
                color=0x48DB01,
                description=f"{self.client.yes} {self.user.mention}: {message}",
            ),
            ephemeral=ephemeral,
        )
class PretendContext(Context):
    flags: Dict[str, Any] = {}

    def __init__(self, **kwargs):
        """Custom commands.Context for the bot"""
        self.ec_emoji = "🏦"
        self.ec_color = 0xD3D3D3
        
        self.w_color = 0xEFBC1B
        self.n_color = 0xFC341B
        self.y_color = 0x48DB01
        self.c_color = 0xcbc3e3
        self.w = "<:warn:1251929429165477948>"
        self.n = "<:deny:1251929424777969797>"
        self.y = "<:check:1251929419795398708>"
        
        super().__init__(**kwargs)

    def __str__(self):
        return f"Pretend bot here in {self.channel.mention}"
    
    async def reply(self, content: Optional[str] = None, *, embed: Optional[discord.Embed] = None, view: Optional[View] = None, mention_author: Optional[bool] = False, file: Optional[discord.File] = discord.utils.MISSING,
        files: Optional[Sequence[discord.File]] = discord.utils.MISSING) -> discord.Message:
   
        reskin = await self.bot.db.fetchrow("SELECT * FROM reskin WHERE user_id = $1 AND toggled = $2", self.author.id, True)
        if reskin != None and reskin['toggled']:
            
            hook = await self.webhook(self.message.channel)
            
            if view == None: return await hook.send(content=content, embed=embed, username=reskin['name'], avatar_url=reskin['avatar'], file=file)
            
            return await hook.send(content=content, embed=embed, username=reskin['name'], avatar_url=reskin['avatar'], view=view, file=file)
        return await self.send(content=content, embed=embed, reference=self.message, view=view, mention_author=mention_author, file=file)
        
    async def send(self, content: Optional[str] = None, *, embed: Optional[discord.Embed] = None, view: Optional[View] = discord.utils.MISSING, mention_author: Optional[bool] = False, allowed_mentions: discord.AllowedMentions = discord.utils.MISSING,  reference: Optional[Union[discord.Message, discord.MessageReference, discord.PartialMessage]] = None, file: Optional[discord.File] = discord.utils.MISSING,
                files: Optional[Sequence[discord.File]] = discord.utils.MISSING) -> discord.Message:
        
        reskin = await self.bot.db.fetchrow("SELECT * FROM reskin WHERE user_id = $1 AND toggled = $2", self.author.id, True)
        if reskin != None and reskin['toggled']:
            
            hook = await self.webhook(self.message.channel)
            return await hook.send(content=content, embed=embed, username=reskin['name'], avatar_url=reskin['avatar'], view=view, allowed_mentions=allowed_mentions, file=file)
        
        return await self.channel.send(content=content, embed=embed, view=view, allowed_mentions=allowed_mentions, reference=reference, mention_author=mention_author, file=file)
  
    async def webhook(self, channel) -> discord.Webhook:
   
        for webhook in await channel.webhooks():
            
            if webhook.user == self.me:
                return webhook
        
        return await channel.create_webhook(name='pretend')

    async def get_attachment(self) -> Optional[Attachment]:
        """get a discord attachment from the channel"""
        if self.message.attachments:
            return self.message.attachments[0]
        if self.message.reference:
            if self.message.reference.resolved.attachments:
                return self.message.reference.resolved.attachments[0]
        messages = [
            mes async for mes in self.channel.history(limit=10) if mes.attachments
        ]
        if len(messages) > 0:
            return messages[0].attachments[0]
        return None

    async def get_sticker(self) -> StickerItem:
        """get a sticker from the channel"""
        if self.message.stickers:
            return self.message.stickers[0]
        if self.message.reference:
            if self.message.reference.resolved.stickers:
                return self.message.reference.resolved.stickers[0]

        messages = [
            message
            async for message in self.channel.history(limit=20)
            if message.stickers
        ]
        if len(messages) > 0:
            return messages[0].stickers[0]
        raise BadArgument("Sticker not found")

    def find_role(self, argument: str) -> Optional[Role]:
        """find a role using it's name"""
        for role in self.guild.roles:
            if role.name == "@everyone":
                continue
            if argument.lower() in role.name.lower():
                return role
        return None

    async def has_reskin(self) -> bool:
        """check if the author has a reskin or not"""
        return (
            await self.bot.db.fetchrow(
                "SELECT * FROM reskin WHERE user_id = $1", self.author.id
            )
            is not None
        )

    async def confirmation_send(self, embed_msg: str, yes_func, no_func) -> Message:
        """Send an embed with confirmation buttons"""
        embed = Embed(color=self.bot.color, description=embed_msg)
        view = ConfirmView(self.author.id, yes_func, no_func)
        return await self.reply(embed=embed, view=view)

    async def economy_send(self, message: str) -> Message:
        """economy cog sending message function"""
        embed = Embed(
            color=self.ec_color,
            description=f"{self.ec_emoji} {self.author.mention}: {message}",
        )
        return await self.reply(embed=embed)

    async def send_warning(self, message: str) -> Message:
        """Send a warning message to the channel"""
        return await self.reply(
            embed=Embed(
                color=self.w_color,
                description=f"{self.w} {self.author.mention}: {message}",
            )
        )

    async def send_error(self, message: str) -> Message:
        """Send an error message to the channel"""
        return await self.reply(
            embed=Embed(
                color=self.n_color,
                description=f"{self.n} {self.author.mention}: {message}",
            )
        )

    async def send_success(self, message: str) -> Message:
        """Send a success message to the channel"""
        return await self.reply(
            embed=Embed(
                color=self.y_color,
                description=f"{self.y} {self.author.mention}: {message}",
            )
        )

    async def pretend_send(self, message: str, **kwargs) -> Message:
        """Send a regular embed message to the channel"""
        return await self.reply(
            embed=Embed(
                color=self.c_color, description=f"{self.author.mention}: {message}"
            ),
            **kwargs,
        )

    async def lastfm_send(self, message: str, reference: Message = None) -> Message:
        """Send a lastfm type message to the channel"""
        return await self.reply(
            embed=Embed(
                color=0xFF0000,
                description=f"<:lastfm:1208752422630064128> {self.author.mention}: {message}",
            )
        )

    async def paginator(self, embeds: List[Union[Embed, str]]) -> Message:
        """Sends some paginated embeds to the channel"""
        if len(embeds) == 1:
            if isinstance(embeds[0], Embed):
                return await self.reply(embed=embeds[0])
            elif isinstance(embeds[0], str):
                return await self.reply(embeds[0])

        paginator = Paginator(self, embeds, self.author.id)
        style = ButtonStyle.gray
        paginator.add_button("prev", emoji="<:prev:1279015499593682995>", style=style)
        paginator.add_button(
            "goto", emoji="<:goto:1279015935784779798>", style=ButtonStyle.blurple
        )
        paginator.add_button("next", emoji="<:next:1279015767857172482>", style=style)
        paginator.add_button(
            "delete", emoji="<:delete:1279015232697663528>", style=ButtonStyle.danger
        )
        await paginator.start()

    async def create_pages(self):
        """Create pages for group commands"""
        return await self.send_help(self.command)

    async def paginate(
        self,
        contents: List[str],
        title: str = None,
        author: dict = {"name": "", "icon_url": None},
    ):
        """Paginate a list of contents in multiple embeds"""
        iterator = [m for m in utils.as_chunks(contents, 10)]
        embeds = [
            Embed(
                color=self.bot.color,
                title=title,
                description="\n".join(
                    [f"`{(m.index(f)+1)+(iterator.index(m)*10)}.` {f}" for f in m]
                ),
            ).set_author(**author)
            for m in iterator
        ]
        return await self.paginator(embeds)
    
class PretendHelp(Help):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_main_help_embed(self, ctx):
        embed = Embed(
            color=self.context.bot.color,
            title="Pretend Command Menu",
            description="```\n"
                        "[ ] = optional, < > = required\n"
                        "Sub commands are indicated by an asterisk(*).\n```",
        )
        embed.add_field(
            name="Useful Links 🔗 ",
            value="**[Support](https://discord.gg/7jUMQ6YnX5)**  • "
                  "**[Website](https://pretend.rip)**  • "
                  "**[Invite](https://discord.com/oauth2/authorize?client_id=1263734958586073141&permissions=8&integration_type=0&scope=bot)**",
            inline=False
        )
        
        return embed

    async def send_bot_help(
        self, mapping: Mapping[Cog | None, List[Command[Any, Callable[..., Any], Any]]]
    ) -> Coroutine[Any, Any, None]:
        bot = self.context.bot
        embed = self.create_main_help_embed(self.context)
        
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.set_footer(text="Select a category from the dropdown menu below")  # Fixed footer
        
        # Log details about the cogs and their commands
        for cog in mapping.keys():
            cog_name = cog.qualified_name if cog else "No Category"
            print(f"Cog Name: {cog_name}, Commands: {len(mapping[cog])}")
        
        # Create a list of categories for the dropdown menu, excluding specific categories
        categories = [
            cog.qualified_name if cog else "No Category"
            for cog in mapping.keys()
            if cog and cog.qualified_name not in ["Owner", "Jishaku", "Members", "API", "Auth", "Messages", "Reactions"]
        ]

        # Log the resulting categories
        print("Categories after filtering:", categories)

        # Handle case where no categories are found
        if not categories:
            categories.append("General")  # Provide a default category if none are found

        # Ensure the number of categories does not exceed 25
        categories = categories[:25]

        # Create the Select menu
        select = Select(
            placeholder="Choose a category...",
            options=[SelectOption(label=category, value=category, description="") for category in categories]
        )

        async def select_callback(interaction: Interaction):
            selected_category = interaction.data['values'][0]
            selected_cog = next((cog for cog in mapping.keys() if (cog and cog.qualified_name == selected_category) or (not cog and selected_category == "No Category")), None)
            
            if selected_cog is not None:
                commands = mapping[selected_cog]
                command_list = ", ".join([f"{command.name}*" if isinstance(command, Group) else f"{command.name}" for command in commands])
            else:
                command_list = "No commands available"
            
            embed = Embed(
                color=self.context.bot.color,
                title=f"Category: {selected_category}",
                description=f"**```\n{command_list}\n```**",
            )
            embed.set_author(name="Pretend Command Menu", icon_url=bot.user.display_avatar.url)
            embed.set_footer(text=f"{len(commands)} command{'s' if len(commands) != 1 else ''}" if selected_cog else "No commands")
            
            await interaction.response.edit_message(embed=embed, view=view)

        select.callback = select_callback

        # Create a View and add the Select menu to it
        view = View()
        view.add_item(select)

        await self.context.reply(embed=embed, view=view)

    def get_desc(self, c: Command | Group) -> str:
        if c.help != None: 
            return c.help.capitalize()
        return "no description"

    async def send_group_help(self, group: Group):
        if (
            group.hidden
            or group.cog_name.lower() == "owner"
            or group.cog_name.lower() == "jishaku"
        ) and self.context.author.id not in self.context.bot.owner_ids:
            return await self.context.send_error(
                "No command called"
                + '"'
                + {self.context.message.content}
                + '"'
                + "found"
            )
        embeds = []
        bot = self.context.bot
        i = 0
        for command in group.commands:
            i += 1
            embeds.append(
                Embed(
                    color=bot.color,
                    title=f"Command: {command.qualified_name}",
                    description=command.help.capitalize() if command.help else None,
                )
                .set_author(name=bot.user.name, icon_url=bot.user.display_avatar.url)
                .add_field(
                    name="usage",
                    value=f"```{command.qualified_name} {' '.join([f'[{a}]' for a in command.clean_params]) if command.clean_params != {} else ''}\n{command.usage or ''}```",
                    inline=False,
                )
                .set_footer(
                    text=f"aliases: {', '.join(a for a in command.aliases) if len(command.aliases) > 0 else 'none'} ・ {i}/{len(group.commands)}"
                )
            )

        await self.context.paginator(embeds)

    async def send_error_message(self, error: str):
        return await self.context.send_error(error)

    async def send_command_help(self, command: Command):
        if (
            command.hidden
            or command.cog_name.lower() == "owner"
            or command.cog_name.lower() == "jishaku"
        ) and self.context.author.id not in self.context.bot.owner_ids:
            return await self.context.send_error(
                "No command called"
                + '"'
                + {self.context.message.content}
                + '"'
                + "found"
            )
        embed = Embed(
            color=self.context.bot.color,
            title=f"Command: {command.qualified_name}",
            description=command.help.capitalize() if command.help else None,
        )
        embed.set_author(
            name=self.context.bot.user.name,
            icon_url=self.context.bot.user.display_avatar.url,
        )
        embed.add_field(name="category", value=command.cog_name.lower())
        embed.add_field(
            name="permissions",
            value=(
                f"{command.brief} {self.context.bot.warning}"
                if command.brief
                else "any"
            ),
        )
        embed.add_field(
            name="usage",
            value=f"```{self.context.clean_prefix}{command.qualified_name} {' '.join([f'[{a}]' for a in command.clean_params]) if command.clean_params != {} else ''}\n{command.usage or ''}```",
            inline=False,
        )
        if command.aliases:
            embed.add_field(
                name="aliases", value=", ".join(command.aliases), inline=False
            )

        await self.context.send(embed=embed)


class Invoking:
    def __init__(self, ctx: PretendContext):
        self.ctx = ctx
        self.variables = {
            "{member}": "the full name of the punished member",
            "{member.name}": "the name of the punished member",
            "{member.discriminator}": "the discriminator of the punished member",
            "{member.id}": "the id of the punished member",
            "{member.mention}": "mentions the punished member",
            "{member.avatar}": "the avatar of the punished member",
            "{reason}": "the reason of the punishment",
        }

    async def send(self, member: Union[User, Member], reason: str):
        ctx = self.ctx
        res = await ctx.bot.db.fetchrow(
            "SELECT embed FROM invoke WHERE guild_id = $1 AND command = $2",
            ctx.guild.id,
            ctx.command.name,
        )
        if res:
            code = res["embed"]
            x = await self.ctx.bot.embed_build.convert(
                ctx, self.invoke_replacement(member, code.replace("{reason}", reason))
            )
            await ctx.reply(**x)
        return res is not None

    async def cmd(self, embed: str) -> Message:
        ctx = self.ctx
        res = await ctx.bot.db.fetchrow(
            "SELECT embed FROM invoke WHERE guild_id = $1 AND command = $2",
            ctx.guild.id,
            ctx.command.name,
        )
        if res:
            code = res["embed"]

            if embed == "none":
                await ctx.bot.db.execute(
                    "DELETE FROM invoke WHERE guild_id = $1 AND command = $2",
                    ctx.guild.id,
                    ctx.command.name,
                )
                return await ctx.send_success(
                    f"Deleted the **{ctx.command.name}** custom response"
                )

            elif embed == "view":
                em = Embed(
                    color=ctx.bot.color,
                    title=f"invoke {ctx.command.name} message",
                    description=f"```{code}```",
                )
                return await ctx.reply(embed=em)

            elif embed == code:
                return await ctx.send_warning(
                    f"This embed is already **configured** as the {ctx.command.name} custom response"
                )

            else:
                await ctx.bot.db.execute(
                    "UPDATE invoke SET embed = $1 WHERE guild_id = $2 AND command = $3",
                    embed,
                    ctx.guild.id,
                    ctx.command.name,
                )
                return await ctx.send_success(
                    f"Updated your custom **{ctx.command.name}** message to ```{embed}```"
                )
        else:
            await ctx.bot.db.execute(
                "INSERT INTO invoke VALUES ($1,$2,$3)",
                ctx.guild.id,
                ctx.command.name,
                embed,
            )
            return await ctx.send_success(
                f"Added your custom **{ctx.command.name}** message as\n```{embed}```"
            )

    def invoke_replacement(self, member: Union[Member, User], params: str = None):
        if params is None:
            return None
        if "{member}" in params:
            params = params.replace("{member}", str(member))
        if "{member.id}" in params:
            params = params.replace("{member.id}", str(member.id))
        if "{member.name}" in params:
            params = params.replace("{member.name}", member.name)
        if "{member.mention}" in params:
            params = params.replace("{member.mention}", member.mention)
        if "{member.discriminator}" in params:
            params = params.replace("{member.discriminator}", member.discriminator)
        if "{member.avatar}" in params:
            params = params.replace("{member.avatar}", member.display_avatar.url)
        return params


class PretendFlags(FlagConverter, prefix="--", delimiter=" ", case_insensitive=True):
    pass
