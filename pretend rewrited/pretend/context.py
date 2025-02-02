from discord.ext import commands
from discord import Embed
from discord.ext.commands import Group
import discord
from discord import Embed, SelectOption, Interaction
from discord.ext import commands
from discord.ui import View, Select

@property
def ping(self) -> int: 
  return round(self.latency * 1000) 

class context(commands.Context): 
 def __init__(self, **kwargs): 
  super().__init__(**kwargs) 

 def find_role(self, name: str): 
   for role in self.guild.roles:
    if role.name == "@everyone": continue  
    if name.lower() in role.name.lower(): return role 
   return None 
 
 async def send_success(self, message: str) -> discord.Message:  
  return await self.reply(embed=discord.Embed(color=0xa3e877, description=f"{self.bot.yes} {self.author.mention}: {message}") )
 
 async def send_error(self, message: str) -> discord.Message: 
  return await self.reply(embed=discord.Embed(color=0xff6465, description=f"{self.bot.no} {self.author.mention}: {message}") ) 
 
 async def send_warning(self, message: str) -> discord.Message: 
  return await self.reply(embed=discord.Embed(color=0xf0c93d., description=f"{self.bot.warning} {self.author.mention}: {message}") )
class EmbedBuilder:
 def ordinal(self, num: int) -> str:
   """Convert from number to ordinal (10 - 10th)""" 
   numb = str(num) 
   if numb.startswith("0"): numb = numb.strip('0')
   if numb in ["11", "12", "13"]: return numb + "th"
   if numb.endswith("1"): return numb + "st"
   elif numb.endswith("2"):  return numb + "nd"
   elif numb.endswith("3"): return numb + "rd"
   else: return numb + "th"    

 def get_parts(params):
    params=params.replace('{embed}', '')
    return [p[1:][:-1] for p in params.split('$v')]

 def embed_replacement(user: discord.Member, params: str=None):
    if params is None: return None
    if '{user}' in params:
        params=params.replace('{user}', str(user.name) + "#" + str(user.discriminator))
    if '{user.mention}' in params:
        params=params.replace('{user.mention}', user.mention)
    if '{user.name}' in params:
        params=params.replace('{user.name}', user.name)
    if '{user.avatar}' in params:
        params=params.replace('{user.avatar}', str(user.display_avatar.url))
    if '{user.joined_at}' in params:
        params=params.replace('{user.joined_at}', discord.utils.format_dt(user.joined_at, style='R'))
    if '{user.created_at}' in params:
        params=params.replace('{user.created_at}', discord.utils.format_dt(user.created_at, style='R'))
    if '{user.discriminator}' in params:
        params=params.replace('{user.discriminator}', user.discriminator)
    if '{guild.name}' in params:
        params=params.replace('{guild.name}', user.guild.name)
    if '{guild.count}' in params:
        params=params.replace('{guild.count}', str(user.guild.member_count))
    if '{guild.count.format}' in params:
        params=params.replace('{guild.count.format}', EmbedBuilder.ordinal(len(user.guild.members)))
    if '{guild.id}' in params:
        params=params.replace('{guild.id}', user.guild.id)
    if '{guild.created_at}' in params:
        params=params.replace('{guild.created_at}', discord.utils.format_dt(user.guild.created_at, style='R'))
    if '{guild.boost_count}' in params:
        params=params.replace('{guild.boost_count}', str(user.guild.premium_subscription_count))
    if '{guild.booster_count}' in params:
        params=params.replace('{guild.booster_count}', str(len(user.guild.premium_subscribers)))
    if '{guild.boost_count.format}' in params:
        params=params.replace('{guild.boost_count.format}', EmbedBuilder.ordinal(user.guild.premium_subscription_count))
    if '{guild.booster_count.format}' in params:
        params=params.replace('{guild.booster_count.format}', EmbedBuilder.ordinal(len(user.guild.premium_subscribers)))
    if '{guild.boost_tier}' in params:
        params=params.replace('{guild.boost_tier}', str(user.guild.premium_tier))
    if '{guild.vanity}' in params: 
        params=params.replace('{guild.vanity}', "/" + user.guild.vanity_url_code or "none")         
    if '{invisible}' in params: 
        params=params.replace('{invisible}', '2f3136') 
    if '{botcolor}' in params: 
        params=params.replace('{botcolor}', '6d827d')       
    if '{guild.icon}' in params:
      if user.guild.icon:
        params=params.replace('{guild.icon}', user.guild.icon.url)
      else: 
        params=params.replace('{guild.icon}', "https://none.none")        

    return params

 async def to_object(params):

    x={}
    fields=[]
    content=None
    view=discord.ui.View()

    for part in EmbedBuilder.get_parts(params):
        
        if part.startswith('content:'):
            content=part[len('content:'):]

        if part.startswith('title:'):
            x['title']=part[len('title:'):]
        
        if part.startswith('description:'):
            x['description']=part[len('description:'):]

        if part.startswith('color:'):
            try:
                x['color']=int(part[len('color:'):].replace("#", ""), 16)
            except:
                x['color']=0x2f3136

        if part.startswith('image:'):
            x['image']={'url': part[len('image:'):]}

        if part.startswith('thumbnail:'):
            x['thumbnail']={'url': part[len('thumbnail:'):]}
        
        if part.startswith('author:'):
            z=part[len('author:'):].split(' && ')
            try:
                name=z[0] if z[0] else None
            except:
                name=None
            try:
                icon_url=z[1] if z[1] else None
            except:
                icon_url=None
            try:
                url=z[2] if z[2] else None
            except:
                url=None

            x['author']={'name': name}
            if icon_url:
                x['author']['icon_url']=icon_url
            if url:
                x['author']['url']=url

        if part.startswith('field:'):
            z=part[len('field:'):].split(' && ')
            try:
                name=z[0] if z[0] else None
            except:
                name=None
            try:
                value=z[1] if z[1] else None
            except:
                value=None
            try:
                inline=z[2] if z[2] else True
            except:
                inline=True

            if isinstance(inline, str):
                if inline == 'true':
                    inline=True

                elif inline == 'false':
                    inline=False

            fields.append({'name': name, 'value': value, 'inline': inline})

        if part.startswith('footer:'):
            z=part[len('footer:'):].split(' && ')
            try:
                text=z[0] if z[0] else None
            except:
                text=None
            try:
                icon_url=z[1] if z[1] else None
            except:
                icon_url=None
            x['footer']={'text': text}
            if icon_url:
                x['footer']['icon_url']=icon_url
                
        if part.startswith('button:'):
            z=part[len('button:'):].split(' && ')
            disabled=True
            style=discord.ButtonStyle.gray
            emoji=None 
            label=None 
            url=None
            for m in z:
             if "label:" in m: label=m.replace("label:", "")
             if "url:" in m: 
                url=m.replace("url:", "").strip()
                disabled=False
             if "emoji:" in m: emoji=m.replace("emoji:", "").strip()
             if "disabled" in m: disabled=True     
             if "style:" in m: 
               if m.replace("style:", "").strip() == "red": style=discord.ButtonStyle.red 
               elif m.replace("style:", "").strip() == "green": style=discord.ButtonStyle.green 
               elif m.replace("style:", "").strip() == "gray": style=discord.ButtonStyle.gray 
               elif m.replace("style:", "").strip() == "blue": style=discord.ButtonStyle.blurple   

            view.add_item(discord.ui.Button(style=style, label=label, emoji=emoji, url=url, disabled=disabled))
            
    if not x: embed=None
    else:
        x['fields']=fields
        embed=discord.Embed.from_dict(x)
    return content, embed, view 

class EmbedScript(commands.Converter): 
  async def convert(self, ctx: commands.Context, argument: str):
   x = await EmbedBuilder.to_object(EmbedBuilder.embed_replacement(ctx.author, argument))
   if x[0] or x[1]: return {"content": x[0], "embed": x[1], "view": x[2]} 
   return {"content": EmbedBuilder.embed_replacement(ctx.author, argument)}

class GoToModal(discord.ui.Modal, title="change the page"):
  page = discord.ui.TextInput(label="page", placeholder="change the page", max_length=3)

  async def on_submit(self, interaction: discord.Interaction) -> None:
   if int(self.page.value) > len(self.embeds): return await interaction.client.ext.send_warning(interaction, f"You can only select a page **between** 1 and {len(self.embeds)}", ephemeral=True) 
   await interaction.response.edit_message(embed=self.embeds[int(self.page.value)-1]) 
  
  async def on_error(self, interaction: discord.Interaction, error: Exception) -> None: 
    await interaction.client.ext.send_warning(interaction, "Unable to change the page", ephemeral=True)
class DropdownHelp(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__()
        self.ctx = ctx
        self.subcommands = ctx.command.commands  # Automatically get the subcommands of the invoked group command
        self.add_item(CommandDropdown(self.subcommands))  # Pass the list of subcommands

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Ensure only the command author can interact with the dropdown
        return interaction.user.id == self.ctx.author.id

class CommandDropdown(discord.ui.Select):
    def __init__(self, commands_list):
        # Create dropdown options for each subcommand
        options = [
            discord.SelectOption(label=cmd.name, description=cmd.short_doc or "No description available")
            for cmd in commands_list
            if not cmd.hidden
        ]
        
        super().__init__(placeholder="Select a command...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Find the selected command by its name
        selected_command = next((cmd for cmd in self.view.subcommands if cmd.name == self.values[0]), None)
        
        if selected_command:
            # Generate detailed embed for the selected command
            embed = discord.Embed(
                title=f"Command: {selected_command.name}",
                description=selected_command.help or "No description available.",
                color=interaction.client.color
            )
            embed.add_field(name="Usage", value=f"```{selected_command.qualified_name}```")
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed)

async def create_pages(ctx: commands.Context):
    """Sends a dropdown menu to navigate subcommands."""
    view = DropdownHelp(ctx)

    # Initial embed to instruct the user
    embed = discord.Embed(
        title=f"{ctx.command.qualified_name.capitalize()} Commands",
        description="Use the **dropdown** below to select a **command** for more **details**.",
        color=ctx.bot.color
    )
    await ctx.send(embed=embed, view=view)


async def getprefix(bot, message):
       if not message.guild: return ";"
       check = await bot.db.fetchrow("SELECT * FROM selfprefix WHERE user_id = $1", message.author.id) 
       if check: selfprefix = check["prefix"]
       res = await bot.db.fetchrow("SELECT * FROM prefixes WHERE guild_id = $1", message.guild.id) 
       if res: guildprefix = res["prefix"]
       else: guildprefix = ";"    
       if not check and res: selfprefix = res["prefix"]
       elif not check and not res: selfprefix = ";"
       return guildprefix, selfprefix 

class GoToModal(discord.ui.Modal, title="change the page"):
  page = discord.ui.TextInput(label="page", placeholder="change the page", max_length=3)

  async def on_submit(self, interaction: discord.Interaction) -> None:
   if int(self.page.value) > len(self.embeds): return await interaction.client.ext.send_warning(interaction, f"You can only select a page **between** 1 and {len(self.embeds)}", ephemeral=True) 
   await interaction.response.edit_message(embed=self.embeds[int(self.page.value)-1]) 
  
  async def on_error(self, interaction: discord.Interaction, error: Exception) -> None: 
    await interaction.client.ext.send_warning(interaction, "Unable to change the page", ephemeral=True)

class PaginatorView(discord.ui.View): 
    def __init__(self, ctx: commands.Context, embeds: list): 
        super().__init__()  
        self.embeds = embeds
        self.ctx = ctx
        self.i = 0

    async def send_success(self, message: str) -> discord.Message:  
        return await self.reply(embed=discord.Embed(color=0xa3e877, description=f"{self.bot.yes} {self.author.mention}: {message}") )
 
    async def send_error(self, message: str) -> discord.Message: 
        return await self.reply(embed=discord.Embed(color=0xff6465, description=f"{self.bot.no} {self.author.mention}: {message}") ) 
 
    async def send_warning(self, message: str) -> discord.Message: 
        return await self.reply(embed=discord.Embed(color=0xf0c93d, description=f"{self.bot.warning} {self.author.mention}: {message}"))
        
    async def send_warning(self, interaction: discord.Interaction, message: str) -> discord.Message:
        return await interaction.response.send_message(
            embed=discord.Embed(color=0xf0c93d, description=f"{self.ctx.bot.warning} {message}"),
            ephemeral=True
        )


    @discord.ui.button(emoji="<:left:1018156480991612999>", style=discord.ButtonStyle.blurple)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button): 
        if interaction.user.id != self.ctx.author.id:
            return await self.send_warning(interaction, "You're not the author of this embed!")          
        if self.i == 0: 
            await interaction.response.edit_message(embed=self.embeds[-1])
            self.i = len(self.embeds) - 1
            return
        self.i -= 1
        await interaction.response.edit_message(embed=self.embeds[self.i])

    @discord.ui.button(emoji="<:right:1018156484170883154>", style=discord.ButtonStyle.blurple)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button): 
        if interaction.user.id != self.ctx.author.id:
            return await self.send_warning(interaction, "You're not the author of this embed!")     
        if self.i == len(self.embeds) - 1: 
            await interaction.response.edit_message(embed=self.embeds[0])
            self.i = 0
            return 
        self.i += 1  
        await interaction.response.edit_message(embed=self.embeds[self.i])

    @discord.ui.button(emoji="<:filter:1039235211789078628>")
    async def goto(self, interaction: discord.Interaction, button: discord.ui.Button): 
        if interaction.user.id != self.ctx.author.id:
            return await self.send_warning(interaction, "You're not the author of this embed!")     
        modal = GoToModal()
        modal.embeds = self.embeds
        await interaction.response.send_modal(modal)

    @discord.ui.button(emoji="<:stop:1018156487232720907>", style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button): 
        if interaction.user.id != self.ctx.author.id:
            return await self.send_warning(interaction, "You are not the author of this embed")     
        await interaction.message.delete()

    async def on_timeout(self) -> None: 
        mes = await self.message.channel.fetch_message(self.message.id)
        if mes is None: return
        if len(mes.components) == 0: return
        for item in self.children:
            item.disabled = True

        try:
            await self.message.edit(view=self)   
        except: pass

class HelpCommand(commands.HelpCommand):
    context: commands.Context

    def __init__(self, **options):
        super().__init__(
            command_attrs={"aliases": ["h", "cmds", "commands"], "hidden": True},
            **options,
        )

    async def send_bot_help(self, _):
        # Filter cogs, excluding specific ones like 'Jishaku' and 'Developer'
        cogs = [
            cog for cog in self.context.bot.cogs.values()
            if cog.get_commands() and cog.qualified_name not in ["Jishaku", "Owner"]
        ]
        
        # Initialize embeds list with an introductory embed
        embeds = [
            Embed(
                color=self.context.bot.color,
                title=("Pretend Help Menu"),
                description=(
                    "Use the buttons below to navigate through categories.\n"
                    "Commands with an asterisk `(*)` are groups with subcommands."
                )
            )
            .set_author(
                name=self.context.bot.user.name,
                icon_url=self.context.bot.user.display_avatar.url,
            )
            .set_thumbnail(url=self.context.bot.user.display_avatar.url)
            .add_field(
                name="Quick Links",
                value=(
                    f"[**Invite**](https://discordapp.com/oauth2/authorize?client_id=1263734958586073141&scope=bot+applications.commands&permissions=8) | "
                    f"[**Support**](https://discord.gg/blonde)"
                ),
                inline=False
            )
            .set_footer(
                text=f"Requested by {self.context.author.name}",
                icon_url=self.context.author.display_avatar.url
            )
        ]
        
        for cog in cogs:
            command_list = "\n".join(
                f" **{cmd.name}{'*' if isinstance(cmd, commands.Group) else ''}** - {cmd.description or 'No description'}"
                for cmd in cog.get_commands() if not cmd.hidden
            )
            embeds.append(
                Embed(
                    color=self.context.bot.color,
                    title=f"{cog.qualified_name} Commands",
                    description=f"Explore commands in the **{cog.qualified_name}** category.\n\n{command_list or 'No commands available.'}",
                )
                .set_author(
                    name=self.context.author.name,
                    icon_url=self.context.author.display_avatar.url,
                )
                .set_thumbnail(url=self.context.bot.user.display_avatar.url)
                .set_footer(
                    text=f"🔍 Category: {cog.qualified_name} • {len(list(cog.walk_commands()))} commands"
                )
            )
        
        # Initialize and use PaginatorView for navigation
        paginator = PaginatorView(self.context, embeds=embeds)
        paginator.message = await self.context.reply(embed=embeds[0], view=paginator)
    async def send_command_help(self, command: commands.Command):
        command_name = f"{str(command.parent)} {command.name}" if str(command.parent) != "None" else command.name

        if command.cog_name == "owner":
            return
        cog_name = command.cog.qualified_name if command.cog else "No Category"

        embed = discord.Embed(
            color=self.context.bot.color,  
            title=f"Command: {command_name}",
            description=command.description or "No description available."
        )

        if command.brief:
            embed.add_field(name="Information", value=f"<:warning:1305212823470866513> {command.brief}", inline=True)

        embed.set_footer(text=f"🔍 Module: {cog_name}")

        embed.add_field(name="Aliases", value=', '.join(map(str, command.aliases)) or "N/A")

        usage_text = f"```{self.context.clean_prefix}{command_name} {command.usage if command.usage else ''}```"
        embed.add_field(name="Usage", value=usage_text, inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group: commands.Group) -> None:
        """Sends a help message for a group command with a dropdown."""
        embed = discord.Embed(
        color=self.context.bot.color,
        title=f"{group.qualified_name} Group Commands",
        description=(
            f"Use the **dropdown** below to view details for **{len(group.commands)} commands** "
            f"in the **{group.qualified_name}** group."
        )
        )
        embed.set_author(
        name=self.context.author.name,
        icon_url=self.context.author.display_avatar.url,
        )
        embed.set_thumbnail(url=self.context.bot.user.display_avatar.url)
        embed.set_footer(text=f"Requested by {self.context.author.name}", icon_url=self.context.author.display_avatar.url)
        view = DropdownHelp(self.context)
        await self.context.reply(embed=embed, view=view)

