import discord
from discord.ext import commands, tasks
from discord import app_commands
import random, asyncio, yaml, os, time
from typing import Literal, Optional
import sqlite3

with open("ymls/collectibles.yml") as f:
    collectibles = yaml.load(f, Loader=yaml.FullLoader)

countryballs = collectibles['countryballs']

with open("config.yml") as f:
    settings = yaml.load(f, Loader=yaml.FullLoader)

token = settings["bot-token"]
prefix = settings["text-prefix"]
collectibles_name = settings["collectibles-name"]
slash_command_name = settings["players-group-cog-name"]
bot_name = settings["bot-name"]
about_description = settings["about"]["description"]
github_link = settings["about"]["github-link"]
discord_invite = settings["about"]["discord-invite"]

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command("help")
tree = bot.tree

caught_balls = {}

conn = sqlite3.connect("caught_balls.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS caught_balls (
        user_id INTEGER,
        url TEXT,
        name TEXT,
        timestamp REAL,
        shiny_status TEXT
    )
""")

def add_caught_ball(user_id, url, name, timestamp, shiny_status):
    cursor.execute("INSERT INTO caught_balls (user_id, url, name, timestamp, shiny_status) VALUES (?, ?, ?, ?, ?)",
                   (user_id, url, name, timestamp, shiny_status))
    conn.commit()

def get_caught_balls_for_user(user_id):
    cursor.execute("SELECT url, name, timestamp FROM caught_balls WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    return rows

def read_config_file():
    config = {}
    if os.path.exists("ymls/configured-channels.yml"):
        with open("ymls/configured-channels.yml", "r") as file:
            config = yaml.safe_load(file) or {}
    return config

configured_channels = read_config_file()

@bot.event
async def on_ready():
    print(f"{time.ctime()} | Logged in as {bot.user.name} ({bot.user.id})")
    print(f"{time.ctime()} | Prefix: {prefix}")
    print(f"{time.ctime()} | Servers: {len(bot.guilds)}")
    print(f"{time.ctime()} | Commands loaded: {len(bot.commands)}")
    await tree.sync()

@tree.command(name="about", description="Get information about this bot.")
async def about(interaction: discord.Interaction):
    total_balls = len(countryballs)
    player_count = cursor.execute("SELECT COUNT(DISTINCT user_id) FROM caught_balls").fetchone()[0]
    total_caught_balls = cursor.execute("SELECT COUNT(*) FROM caught_balls").fetchone()[0]

    embed = discord.Embed(
        title=f"{bot_name}",
        description=f"""
{about_description}
Currently running version [1.5](https://github.com/wascertified/dockerless-dex/releases/tag/1.5)

{total_balls} {collectibles_name}s to collect
{player_count} players that caught {total_caught_balls} {collectibles_name}s
{len(bot.guilds)} servers playing

This bot was made/coded by wascertified. The github is https://github.com/wascertified

Support Server: {discord_invite}
        """,
        color=discord.Color.blurple()
    )
    await interaction.response.send_message(embed=embed)

@tree.command(name=f"{slash_command_name}_list", description=f"List your {collectibles_name}s.")
async def list_collectibles(interaction: discord.Interaction):
    caught_balls = get_caught_balls_for_user(interaction.user.id)
    if caught_balls:
        embed = discord.Embed(
            title=f"Your {collectibles_name}",
            description="Here is what you own:",
            color=discord.Color.blue()
        )
        for url, name, timestamp in caught_balls:
            embed.add_field(name=name.capitalize(), value=f"Caught at: <t:{int(timestamp)}:F>", inline=False)
    else:
        embed = discord.Embed(
            title=f"No {collectibles_name}s found.",
            description=f"You haven't caught any {collectibles_name}s yet!",
            color=discord.Color.red()
        )
    await interaction.response.send_message(embed=embed)
    
@tree.command(name=f"{slash_command_name}_completion", description=f"Show your current completion of {bot_name}.")
async def completion(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user

    username = member.display_name
    user_id = member.id

    owned_balls = get_caught_balls_for_user(user_id)
    user_owned_balls = {ball[1]: ball[0] for ball in owned_balls}

    all_balls_data = countryballs.items()

    if not all_balls_data:
        await interaction.response.send_message(f"No {collectibles_name} added yet.")
        return
        
    with open('ymls/collectibles.yml', 'r') as emojis_file:
        ball_to_emoji = yaml.safe_load(emojis_file).get("ball_to_emoji", {})

    embed = discord.Embed(
        title=f"{username}'s",
        description=f"{bot_name} progression: **{len(user_owned_balls)/len(all_balls_data)*100:.2f}%**",
        color=discord.Color.blurple(),
    ).set_thumbnail(url=member.avatar.url)

    if user_owned_balls:
        owned_list = ' '.join([ball_to_emoji.get(name, '') or name.capitalize() for name in user_owned_balls.keys()])
        embed.add_field(name=f"Owned {collectibles_name}s", value=owned_list, inline=False)
    else:
        embed.add_field(name=f"Owned {collectibles_name}s", value=f"No owned {collectibles_name}s yet.", inline=False)

    missing_balls = [(name, url) for name, url in all_balls_data if name not in user_owned_balls]

    if missing_balls:
        missing_list = ' '.join([ball_to_emoji.get(name, '') or f"[{name.capitalize()}]({url})" for name, url in missing_balls])
        embed.add_field(name=f"Missing {collectibles_name}s", value=missing_list, inline=False)
    else:
        embed.add_field(name=f"Missing {collectibles_name}s", value=f"", inline=False)

    await interaction.response.send_message(embed=embed)

@tree.command(name=f'{slash_command_name}_config', description='Configure a spawn channel for the server.')
@commands.has_permissions(manage_channels=True)
async def config(interaction: discord.Interaction, channel: discord.TextChannel):
    channel_id = channel.id
    if interaction.guild_id in configured_channels:
        await interaction.response.send_message(f"A spawn channel is already configured for this server. Use /{slash_command_name}_disableconfig to remove it.")
    else:
        configured_channels[interaction.guild_id] = channel_id
        with open('ymls/configured-channels.yml', 'w') as config_file:
            yaml.dump({interaction.guild_id: channel_id}, config_file, default_flow_style=False)
        embed = discord.Embed(
            title=f"{bot_name} Activation",
            description=f"{bot_name} is now configured in {channel.mention}! To remove this spawn channel, use the `/{slash_command_name}_disableconfig` command.\n\n"
                        "[Terms of Service](https://gist.github.com/laggron42/52ae099c55c6ee1320a260b0a3ecac4e)",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

@tree.command(name=f'{slash_command_name}_disableconfig', description='Disable the spawn channel for the server.')
@commands.has_permissions(administrator=True)
async def disableconfig(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    if guild_id in configured_channels:
        del configured_channels[guild_id]
        
        with open('ymls/configured-channels.yml', 'r') as config_file:
            config_dict = yaml.safe_load(config_file) or {}

        if str(guild_id) in config_dict:
            del config_dict[str(guild_id)]
         
        with open('ymls/configured-channels.yml', 'w') as config_file:
            yaml.dump(config_dict, config_file, default_flow_style=False)
        
        await interaction.response.send_message(f"{bot_name} spawn channel configuration has been removed for this server.")
    else:
        await interaction.response.send_message("No spawn channel is currently configured for this server.")

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def reloadtree(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} tree commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}")

@tree.command(name="ping", description="Ping the bot.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! {}ms".format(round(bot.latency * 1000)))

@bot.command()
@commands.is_owner()
async def kill(ctx):
    await ctx.send("dying!! 😭")
    await bot.close()

@bot.command()
@commands.is_owner()
async def giveball(ctx, user: discord.User, url: str):
    ballname = url.split('/')[-1].split('.')[0]
    if ballname not in countryballs:
        await ctx.send(f"The {collectibles_name} with name \"{ballname}\" does not exist.")
        return

    shiny_status = "No"
    timestamp = time.time()
    add_caught_ball(user.id, url, ballname, timestamp, shiny_status)
    await ctx.send(f"The \"{ballname}\" {collectibles_name} was given to {user.display_name}.")

class CatchModal(discord.ui.Modal):
    def __init__(self, countryball_name, countryball_url, catch_button):
        super().__init__(title=f'Catch the {collectibles_name}!')
        self.correct_name = countryball_name
        self.countryball_url = countryball_url
        self.catch_button = catch_button
        self.countryball_name_input = discord.ui.TextInput(
            label=f'Name this {collectibles_name}!',
            style=discord.TextStyle.short,
            placeholder=f'What is the name of this {collectibles_name}',
            required=True
        )
        self.add_item(self.countryball_name_input)

    async def on_submit(self, interaction: discord.Interaction):
        if self.catch_button.disabled:
            await interaction.response.send_message(f"{interaction.user.mention} I've been caught already!", ephemeral=False)
            return

        user_owns_ball = check_if_user_owns_ball(interaction.user.id, self.correct_name)
        shiny_status = "Yes" if random.randint(1, 2048) == 1 else "No"
        shiny_message = f"\n⭐ **It's a shiny {collectibles_name}** ⭐" if shiny_status == "Yes" else ""

        if self.countryball_name_input.value.lower() == self.correct_name.lower():
            add_caught_ball(interaction.user.id, self.countryball_url, self.correct_name, time.time(), shiny_status)
            message_content = f"{interaction.user.mention} You caught **{self.correct_name}!**"
            if not user_owns_ball:
                message_content += f"\n\nThis is a **new {collectibles_name}** that has been added to your collection!"
            message_content += shiny_message
            await interaction.response.send_message(message_content, ephemeral=False)
            self.catch_button.disabled = True
            self.catch_button.label = "Caught!"
            await interaction.message.edit(view=self.catch_button.view)
        else:
            await interaction.response.send_message(f"{interaction.user.mention} Wrong name! You wrote: {self.countryball_name_input}", ephemeral=False)

def check_if_user_owns_ball(user_id, ball_name):
    """
    Check if the user already owns the specified ball.

    Parameters:
    - user_id: The ID of the user.
    - ball_name: The name of the ball to check.

    Returns:
    True if the user owns the ball, or False otherwise.
    """
    owned_balls = get_caught_balls_for_user(user_id)
    return any(ball[1].lower() == ball_name.lower() for ball in owned_balls)

spawned_balls = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id in configured_channels.values():
        await try_spawning_countryball(message)

    await bot.process_commands(message)

async def try_spawning_countryball(message):
    last_spawn_info = spawned_balls.get(message.channel.id)
    current_time = time.time()

    # if the bot hasn't spawned anything in the last hour, spawn a new ball
    if last_spawn_info is None or current_time - last_spawn_info.get('timestamp', 0) >= 3600:
        await spawn_countryball(message.channel)

async def spawn_countryball(channel):
    countryball_choice = random.choice(list(countryballs.items()))
    random_countryball_name, random_countryball_url = countryball_choice

    embed = discord.Embed(
        title=f"A wild {collectibles_name} appeared!"
    )
    embed.set_image(url=random_countryball_url)

    view = discord.ui.View()
    catch_button = discord.ui.Button(label="Catch me!", style=discord.ButtonStyle.primary)
    
    async def catch_button_callback(interaction):
        await interaction.response.send_modal(
            CatchModal(random_countryball_name, random_countryball_url, catch_button)
        )
    catch_button.callback = catch_button_callback
    view.add_item(catch_button)

    try:
        message = await channel.send(embed=embed, view=view)
        spawned_balls[channel.id] = {
            'url': random_countryball_url,
            'name': random_countryball_name,
            'timestamp': time.time(),
            'channel_id': channel.id
        }
    except discord.HTTPException as e:
        print(f"Failed to send message: {e}")
    except discord.InvalidArgument as e:
        print(f"Invalid argument: {e}")

@bot.command()
@commands.is_owner()
async def spawnball(ctx, *, ball_name: str = None):
    channel = ctx.channel
    if ball_name:
        random_countryball_name = ball_name
        random_countryball_url = countryballs.get(ball_name)
        if not random_countryball_url:
            await ctx.send(f"No {collectibles_name} found with name: {ball_name}")
            return
    else:
        countryball_choice = random.choice(list(countryballs.items()))
        random_countryball_name, random_countryball_url = countryball_choice

    embed = discord.Embed(
        title=f"A wild {collectibles_name} appeared!"
    )
    embed.set_image(url=random_countryball_url)

    view = discord.ui.View()
    catch_button = discord.ui.Button(label="Catch me!", style=discord.ButtonStyle.primary)

    async def catch_button_callback(interaction):
        bot.loop.create_task(
            interaction.response.send_modal(
                CatchModal(random_countryball_name, random_countryball_url, catch_button)
            )
        )

    catch_button.callback = catch_button_callback
    view.add_item(catch_button)

    try:
        message = await channel.send(embed=embed, view=view)
        caught_balls[message.id] = {
            'url': random_countryball_url,
            'name': random_countryball_name,
            'timestamp': time.time(),
            'channel_id': channel.id
        }
    except discord.HTTPException as e:
        await ctx.send(f"Failed to send message: {e}")

if not token:
    print("No token was found in config.yml! Please check your settings.")
    exit()
elif not isinstance(token, str) or len(token) == 0:
    print("Invalid token, was found, check your settings!")
    exit()

if not prefix:
    print("No prefix was found in settings.yml! Please check your settings.")
    exit()

if not collectibles_name:
    print("No collectibles name was found in settings.yml! Please check your settings.")
    exit()

if not slash_command_name:
    print("No players group cog name was found in settings.yml! Please check your settings.")
    exit()

if not bot_name:
    print("No bot name was found in settings.yml! Please check your settings.")
    exit()
  
bot.run(token)