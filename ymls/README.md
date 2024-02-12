# YMLS/ FOLDER
In this README markdown file I'll teach you some stuff about the YMLS, so you're good to go once you decide if you want to selfhost.

## emojis.yml
In this file you'll have something that looks like this:
```yml
ball_to_emoji:
  ball 1: emoji
  ball 2: emoji again

# note, it doesnt need the ID, it needs the ACTUAL emoji id (something like <:full_rat:1205271877245730878>), you can get it by doing \:emoji_name: please note that it is CasE SensItivE
```
The YML file above is the main thing that makes the collectibles have their emojis at /completion.

This is what it would look like if we were to add a "full rat" ball.
```yml
ball_to_emoji:
  full rat: <:full_rat:1205271877245730878>
#  ball 2: emoji again

# NOTE: The ball needs to be in bot.py with a working image link.
```
You can see the "ball 2" has been "removed". This is so there aren't any issues. If you were to have two collectibles, you could safely replicate what we did in the first line. *(You obviously need to change "ball 2" to your other added ball in [dex.py](https://github.com/wascertified/dockerless-dex/blob/main/dex.py) and also change "emoji again" to your actual emoji ID.)*

This is what the top of our [dex.py](https://github.com/wascertified/dockerless-dex/blob/main/dex.py) file would look like:
```py
countryballs = {
 "full rat": "https://bigrat.monster/media/perfect.png"
# "ball name 2": "ball url 2"
# add more if you want, this is just an example.
}
```
> [!NOTE]
> A `,` is required after adding the first ball. E.G:
> ```py
> countryballs = {
>  "ball name": "ball url", # < Comma
>  "ball name2": "ball url2"
> }
> ```
> As you can see, the second line doesn't have the `,` like the first one.

## configured-channels.yml
The name should explain itself. But basically; this is where the spawn channels are stored.

The format is something like this:
```yml
Guild ID: Channel ID
Guild ID: Channel ID
``` 
## config.yml
The configuration file. Editing this file is **required** to edit **no matter what**.

Here's the file: *(For previewing.)*
```yml
# Welcome to the config file. Please read the README.md file found at the ymls folder.

bot-token: "Your Token Here" # The bot token for your bot.
text-prefix: "b." # The prefix for text commands. They can be found at the README file mentioned above.

# Stuff that will be shown on /about.
about:
  description: "Collect balls on Discord. Made for people without docker / pc" # Main description. I recommend editing the /about command directly.
  github-link: "https://github.com/wascertified/dockerless-dex" # Only change this if you have a fork, this is not required and can be skipped.
  discord-invite: "https://discord.gg/RSdcTAn7FG" # Change to your discord server.

# Stuff that will be used on commands.
collectibles-name: "ball" # Don't add an "s" as the bot will already add the extra "s".
bot-name: "Dockerless-Dex" # The name of the dex.
players-group-cog-name: "balls" # No spaces, must be lowercase.
```
> [!NOTE]
> The `bot-token` is required. You can find the the proccess of getting your token [here](https://youtu.be/watch?v=aI4OmIbkJH8).

### What Does This Do?
This section is for seeing what X thing does.
#### Main
1. bot-token
   - Tells `dex.py` the discord bot token so it can run it.
2. text-prefix
   - The prefix for text-based commands. Some of them include `giveball`, `spawnball`, and `reloadtree`.
     - `giveball {user} {valid_collectable}` | {user} must be a user mention or user ID.
     - `spawnball {valid_collectable}` | The collectable is optional.
     - `reloadtree` | Reloads trees. *(slash commands)*
#### /about Section
1. description
   - The text that will be shown at the start of `/about`.
2. github-link
   - Changes the github link present in `/about`. It is not required to edit this nor to make a fork.
3. discord-invite
   - Changes the discord invite present in `/about`. Defaults to the support server, change if you have an official server.
#### Commands Section
1. collectibles-name
   - Changes the messages in the bot to refer to your collectables. E.G: You caught a new ball!
2. bot-name
   - Changes the messages in the bot to refer to your bot. E.G: Dockerless-Dex will start spawning balls in this channel. *(Not an actual message inside the bot, but you get the point.)*
3. players-group-cog-name
   - Changes the begginning of the commands for your bot. E.G: /balls_list *(Please note that it can only be lowercase and can't contain spaces.)*
