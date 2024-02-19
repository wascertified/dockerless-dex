import discord
from discord.ext import commands, tasks
from discord import app_commands
import random, asyncio, yaml, os, time
from typing import Literal, Optional
import sqlite3

with open("ymls/collectibles.yml") as f:
    collectibles = yaml.load(f, Loader=yaml.FullLoader)

countryballs = collectibles['countryballs']
catch_names = collectibles['catch_names']

with open("config.yml") as f:
    settings = yaml.load(f, Loader=yaml.FullLoader)

with open('ymls/collectibles.yml', 'r') as emojis_file:
    ball_to_emoji = yaml.safe_load(emojis_file).get("ball_to_emoji", {})

with open('ymls/rarities.yml', 'r') as file:
    rarities = yaml.safe_load(file)['rarities']

token = settings["bot-token"]
prefix = settings["text-prefix"]
collectibles_name = settings["collectibles-name"]
slash_command_name = settings["players-group-cog-name"]
bot_name = settings["bot-name"]
about_description = settings["about"]["description"]
github_link = settings["about"]["github-link"]
discord_invite = settings["about"]["discord-invite"]
authorized_users = settings["authorized-users"]
startup_status = settings.get('startup_status', {})
activity_type = startup_status.get('activity_type', 'playing')
activity_name = startup_status.get('activity_name', '')
status = startup_status.get('status', 'online')
stream_url = startup_status.get('stream_url', '')

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
        shiny_status TEXT,
        hp INTEGER,
        attack INTEGER
    )
""")

def check_authorized(ctx):
  return ctx.author.id in authorized_users

def add_caught_ball(user_id, url, name, timestamp, shiny_status, hp, attack):
    cursor.execute("INSERT INTO caught_balls (user_id, url, name, timestamp, shiny_status, hp, attack) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (user_id, url, name, timestamp, shiny_status, hp, attack))
    conn.commit()

def get_caught_balls_for_user(user_id):
    cursor.execute("SELECT url, name, timestamp, shiny_status, hp, attack FROM caught_balls WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    return rows

cursor.execute("""
    CREATE TABLE IF NOT EXISTS blacklist (
        id INTEGER PRIMARY KEY,
        entity_id INTEGER,
        entity_type TEXT,
        reason TEXT
    )
""")

discord_status = getattr(discord.Status, status, discord.Status.online)
if activity_type == 'playing':
    activity = discord.Game(name=activity_name)
elif activity_type == 'streaming':
    activity = discord.Streaming(name=activity_name, url=stream_url)
elif activity_type == 'listening':
    activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
elif activity_type == 'watching':
    activity = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
else:
    activity = None

db_path = "blacklist.db"
if not os.path.exists(db_path):
    open(db_path, 'a').close()

def add_to_blacklist(entity_id, entity_type, reason):
    cursor.execute("INSERT INTO blacklist (entity_id, entity_type, reason) VALUES (?, ?, ?)",
                   (entity_id, entity_type, reason))
    conn.commit()

def remove_from_blacklist(entity_id, entity_type):
    cursor.execute("DELETE FROM blacklist WHERE entity_id = ? AND entity_type = ?",
                   (entity_id, entity_type))
    conn.commit()

def is_blacklisted(entity_id, entity_type):
    cursor.execute("SELECT * FROM blacklist WHERE entity_id = ? AND entity_type = ?",
                   (entity_id, entity_type))
    return cursor.fetchone() is not None

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
    await bot.change_presence(status=discord_status, activity=activity)
    await tree.sync()

@bot.command()
@commands.check(check_authorized)
async def blacklist(ctx, user: discord.User, *, reason: str):
    if not is_blacklisted(user.id, 'user'):
        add_to_blacklist(user.id, 'user', reason)
        await ctx.send(f"{user.mention} has been blacklisted for reason: {reason}")
    else:
        await ctx.send(f"{user.mention} is already blacklisted.")

@bot.command()
@commands.check(check_authorized)
async def serverblacklist(ctx, server: discord.Guild, *, reason: str):
    if not is_blacklisted(server.id, 'server'):
        add_to_blacklist(server.id, 'server', reason)
        await ctx.send(f"{server.name} has been blacklisted for reason: {reason}")
    else:
        await ctx.send(f"{server.name} is already blacklisted.")

@bot.command()
@commands.check(check_authorized)
async def blacklistremove(ctx, user: discord.User):
    if is_blacklisted(user.id, 'user'):
        remove_from_blacklist(user.id, 'user')
        await ctx.send(f"{user.mention} has been removed from the blacklist.")
    else:
        await ctx.send(f"{user.mention} is not blacklisted.")

@bot.command()
@commands.check(check_authorized)
async def serverblacklistremove(ctx, server: discord.Guild):
    if is_blacklisted(server.id, 'server'):
        remove_from_blacklist(server.id, 'server')
        await ctx.send(f"{server.name} has been removed from the blacklist.")
    else:
        await ctx.send(f"{server.name} is not blacklisted.")

@tree.command(name="about", description="Get information about this bot.")
async def about(interaction: discord.Interaction):
    user_id = interaction.user.id
    guild_id = interaction.guild_id
    if is_blacklisted(user_id, 'user') or (guild_id and is_blacklisted(guild_id, 'server')):
        await interaction.response.send_message("You or this server are blacklisted from using this bot.", ephemeral=True)
        return

    total_balls = len(countryballs)
    player_count = cursor.execute("SELECT COUNT(DISTINCT user_id) FROM caught_balls").fetchone()[0]
    total_caught_balls = cursor.execute("SELECT COUNT(*) FROM caught_balls").fetchone()[0]
    
    if total_balls < 16:
        balls_to_show = " ".join(random.choices(list(ball_to_emoji.values()), k=total_balls))
    elif total_balls == 1:
        balls_to_show = " ".join(random.choices(list(ball_to_emoji.values()), k=1))
    else:
        balls_to_show = " ".join(random.choices(list(ball_to_emoji.values()), k=16))

    embed = discord.Embed(
        title=f"{bot_name}",
        description=f"""
{balls_to_show}
{about_description}
Currently running version [1.8](https://github.com/wascertified/dockerless-dex/releases/tag/1.8)

{total_balls} {collectibles_name}s to collect
{player_count} players that caught {total_caught_balls} {collectibles_name}s
{len(bot.guilds)} servers playing

This bot was made/coded by wascertified.

[Discord Server]({discord_invite}) | [GitHub]({github_link}) | [Invite me!](https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot+applications.commands)
        """,
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=bot.user.avatar.url)
    await interaction.response.send_message(embed=embed)

@tree.command(name=f"{slash_command_name}_list", description=f"List your {collectibles_name}s.")
async def list(interaction: discord.Interaction, user: discord.Member = None):
    user_id = interaction.user.id
    guild_id = interaction.guild_id
    if is_blacklisted(user_id, 'user') or (guild_id and is_blacklisted(guild_id, 'server')):
        await interaction.response.send_message("You or this server are blacklisted from using this bot.", ephemeral=True)
        return

    if user is None:
        user = interaction.user
    caught_balls = get_caught_balls_for_user(user.id)
    embed = discord.Embed(
        title=f"{user.display_name}'s {collectibles_name}",
        color=discord.Color.blue() if caught_balls else discord.Color.red()
    )
    if caught_balls:
        embed.description = "Here is what they own:"
        for url, name, timestamp, shiny_status, _, _ in caught_balls:
            try:
                if shiny_status:
                    emoji_id = ":star:"
                else:
                    emoji_id = ball_to_emoji.get(name)
                name_with_emoji = f"{emoji_id} | {name.capitalize()}" if emoji_id else name.capitalize()
                embed.add_field(name=name_with_emoji, value=f"Caught at: <t:{int(timestamp)}:F>", inline=False)
            except ValueError as ve:
                print(f"Invalid ball information format: {ve}")
                continue
    else:
        embed.description = f"They haven't caught any {collectibles_name}s yet!"
    await interaction.response.send_message(embed=embed)

@tree.command(name=f"{slash_command_name}_completion", description=f"Show your current completion of {bot_name}.")
async def completion(interaction: discord.Interaction, member: discord.Member = None):
    user_id = interaction.user.id
    guild_id = interaction.guild_id
    if is_blacklisted(user_id, 'user') or (guild_id and is_blacklisted(guild_id, 'server')):
        await interaction.response.send_message("You or this server are blacklisted from using this bot.", ephemeral=True)
        return

    if member is None:
        member = interaction.user

    username = member.display_name

    owned_balls = get_caught_balls_for_user(user_id)
    user_owned_balls = {ball[1]: ball[0] for ball in owned_balls}

    all_balls_data = countryballs.items()

    if not all_balls_data:
        await interaction.response.send_message(f"No {collectibles_name}s added yet.")
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

@tree.command(name=f"{slash_command_name}_rarity", description=f"Show the rarity of all the {collectibles_name}s!")
async def rarity(interaction: discord.Interaction): 
    with open('ymls/rarities.yml', 'r') as file:
        rarities = yaml.safe_load(file)['rarities']

    with open('ymls/collectibles.yml', 'r') as emojis_file:
        ball_to_emoji = yaml.safe_load(emojis_file).get("ball_to_emoji", {})

    sorted_rarities = sorted(rarities.items(), key=lambda item: item[1])

    items_per_page = 7
    pages = [sorted_rarities[i:i + items_per_page] for i in range(0, len(sorted_rarities), items_per_page)]
    current_page = 0

    def create_embed(page_index):
        embed = discord.Embed(
            title=f"{collectibles_name.capitalize}s rarities:",
            color=discord.Color.blurple(),
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        for name, rarity_value in pages[page_index]:
            emoji = ball_to_emoji.get(name, '')
            embed.add_field(name=name.capitalize(), value=f"{emoji} Rarity: {rarity_value}", inline=False)
        return embed

    view = discord.ui.View()

    async def previous_page(interaction):
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            await interaction.response.edit_message(embed=create_embed(current_page), view=view)

    async def next_page(interaction):
        nonlocal current_page
        if current_page < len(pages) - 1:
            current_page += 1
            await interaction.response.edit_message(embed=create_embed(current_page), view=view)

    previous_button = discord.ui.Button(label="Back", style=discord.ButtonStyle.primary, disabled=True)
    next_button = discord.ui.Button(label="Next", style=discord.ButtonStyle.primary)

    if len(pages) <= 1:
        next_button.disabled = True

    previous_button.callback = previous_page
    next_button.callback = next_page

    view.add_item(previous_button)
    view.add_item(next_button)

    await interaction.response.send_message(embed=create_embed(current_page), view=view)

@tree.command(name=f'{slash_command_name}_config', description='Configure a spawn channel for the server.')
@commands.has_permissions(manage_channels=True)
async def config(interaction: discord.Interaction, channel: discord.TextChannel):
    user_id = interaction.user.id
    guild_id = interaction.guild_id
    if is_blacklisted(user_id, 'user') or (guild_id and is_blacklisted(guild_id, 'server')):
        await interaction.response.send_message("You or this server are blacklisted from using this bot.", ephemeral=True)
        return

    channel_id = channel.id
    if interaction.guild_id in configured_channels:
        await interaction.response.send_message(f"A spawn channel is already configured for this server. Use /{slash_command_name}_disableconfig to remove it.")
    else:
        configured_channels[interaction.guild_id] = channel_id
        with open('ymls/configured-channels.yml', 'w') as config_file:
            yaml.dump({interaction.guild_id: channel_id}, config_file, default_flow_style=False)
        embed = discord.Embed(
            title=f"{bot_name.capitalize} Activation",
            description=f"{bot_name} is now configured in {channel.mention}! To remove this spawn channel, use the `/{slash_command_name}_disableconfig` command.\n\n"
                        "[Terms of Service](https://gist.github.com/laggron42/52ae099c55c6ee1320a260b0a3ecac4e)",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)

@tree.command(name=f'{slash_command_name}_disableconfig', description='Disable the spawn channel for the server.')
@commands.has_permissions(manage_channels=True)
async def disableconfig(interaction: discord.Interaction):
    user_id = interaction.user.id
    guild_id = interaction.guild_id
    if is_blacklisted(user_id, 'user') or (guild_id and is_blacklisted(guild_id, 'server')):
        await interaction.response.send_message("You or this server are blacklisted from using this bot.", ephemeral=True)
        return

    guild_id = interaction.guild_id
    if guild_id in configured_channels:
        del configured_channels[guild_id]
        
        with open('ymls/configured-channels.yml', 'r') as config_file:
            config_dict = yaml.safe_load(config_file) or {}

        if str(guild_id) in config_dict:
            del config_dict[str(guild_id)]
         
        with open('ymls/configured-channels.yml', 'w') as config_file:
            yaml.dump(config_dict, config_file, default_flow_style=False)
        
        await interaction.response.send_message(f"{bot_name.capitalize} spawn channel configuration has been removed for this server.")
    else:
        await interaction.response.send_message("No spawn channel is currently configured for this server.")

@bot.command()
@commands.guild_only()
@commands.check(check_authorized)
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
    user_id = interaction.user.id
    guild_id = interaction.guild_id
    if is_blacklisted(user_id, 'user') or (guild_id and is_blacklisted(guild_id, 'server')):
        await interaction.response.send_message("You or this server are blacklisted from using this bot.", ephemeral=True)
        return

    await interaction.response.send_message("Pong! {}ms".format(round(bot.latency * 1000)))

@bot.command(aliases=["kill"])
@commands.check(check_authorized)
async def shutdown(ctx):
    await ctx.send("Shutting down.")
    await bot.close()

@bot.command()
@commands.check(check_authorized)
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
        self.stats = {}

    async def on_submit(self, interaction: discord.Interaction):
        if self.catch_button.disabled:
            await interaction.response.send_message(f"{interaction.user.mention} I've been caught already!", ephemeral=False)
            return

        input_name = self.countryball_name_input.value.lower()
        correct_catch_names = {name.lower() for name_list in catch_names.values() for name in (name_list if isinstance(name_list, type([])) else [name_list])}
        correct_catch_name = input_name in correct_catch_names

        if self.correct_name.lower() == "ball 1":
            self.stats['hp'] = random.randint(600, 610)
            self.stats['attack'] = random.randint(760, 770)
        else:
            self.stats['hp'] = random.randint(50, 60)
            self.stats['attack'] = random.randint(75, 85)

        user_owns_ball = check_if_user_owns_ball(interaction.user.id, self.correct_name)
        shiny_status = "Yes" if random.randint(1, 2048) == 1 else "No"
        shiny_message = f"\n:star: It's a shiny **{collectibles_name}**! :star:" if shiny_status == "Yes" else ""

        if correct_catch_name and input_name in correct_catch_names:
            add_caught_ball(interaction.user.id, self.countryball_url, self.correct_name, time.time(), shiny_status, self.stats['hp'], self.stats['attack'])
            message_content = f"{interaction.user.mention} You caught **{self.correct_name}!** (attack: {self.stats['attack']}, hp: {self.stats['hp']})"
            if not user_owns_ball:
                message_content += f"\n\nThis is a **new {collectibles_name}** that has been added to your collection!"
            message_content += shiny_message
            await interaction.response.send_message(message_content, ephemeral=False)
            self.catch_button.disabled = True
            self.catch_button.label = "Caught!"
            await interaction.message.edit(view=self.catch_button.view)
        else:
            await interaction.response.send_message(f"{interaction.user.mention} Wrong name! You wrote: **{self.countryball_name_input}**", ephemeral=False)

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

weighted_countryballs = [name for name, rarity in rarities.items() for _ in range(int(rarity))]

async def spawn_countryball(channel):
    random_countryball_name = random.choices(weighted_countryballs, k=1)[0]
    random_countryball_url = countryballs[random_countryball_name]

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
@commands.check(check_authorized)
async def spawnball(ctx, *, ball_name: str = None):
    channel = ctx.channel
    if ball_name:
        random_countryball_name = ball_name
        random_countryball_url = countryballs.get(ball_name)
        if not random_countryball_url:
            await ctx.send(f"No {collectibles_name} found with name: {ball_name}!")
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
        
@bot.command(aliases=["stat"])
@commands.check(check_authorized)
async def status(ctx, action: str, *args):
    if action == "set":
        activity_type, *activity_details = args
        if activity_type.lower() == "streaming":
            activity = discord.Streaming(name=" ".join(activity_details), url="http://twitch.tv/streamer")
        elif activity_type.lower() == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=" ".join(activity_details))
        elif activity_type.lower() == "playing":
            activity = discord.Game(name=" ".join(activity_details))
        else:
            await ctx.send("Unsupported activity type. Avaible are `streaming`, `watching`, and `playing`.")
            return
        await bot.change_presence(activity=activity)
        await ctx.send(f"Status set to {activity_type} {' '.join(activity_details)}")
    elif action == "remove":
        await bot.change_presence(activity=None, status=discord.Status.online)  # Reset to online when removing activity
        await ctx.send("Status removed.")
    elif action == "simple":
        status_type = args[0].lower()
        if status_type == "dnd":
            await bot.change_presence(status=discord.Status.dnd)
        elif status_type == "online":
            await bot.change_presence(status=discord.Status.online)
        elif status_type == "invisible":
            await bot.change_presence(status=discord.Status.invisible)
        elif status_type == "idle":
            await bot.change_presence(status=discord.Status.idle)
        else:
            await ctx.send("Invalid status type. Avaible are `dnd`, `online`, `invisible`, and `idle`.")
            return
        await ctx.send(f"Status set to {status_type.capitalize()}.")
    else:
        await ctx.send("Invalid action. Avaible are `set`, `remove`, and `simple`. Simply use any of the mentioned without other arguments to see avaible options.")

if not token:
    print("No token was found in config.yml! Please check your settings.")
    exit()
elif not isinstance(token, str) or len(token) == 0:
    print("Invalid token, was found, check your settings!")
    exit()

if not prefix:
    print("No prefix was found in config.yml! Please check your settings.")
    exit()

if not collectibles_name:
    print("No collectibles name was found in config.yml! Please check your settings.")
    exit()

if not slash_command_name:
    print("No players group cog name was found in config.yml! Please check your settings.")
    exit()

if not bot_name:
    print("No bot name was found in config.yml! Please check your settings.")
    exit()
  
bot.run(token)
