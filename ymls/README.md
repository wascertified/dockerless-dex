# YMLS/ FOLDER
In this README markdown file I'll teach you some stuff about the YMLS, so you're good to go once you decide if you want to selfhost.

## collectibles.yml
This YML file is where you will add your collectables. Since you just cloned the repo *(or downloaded it)*, your file will probably look something like this:
```yml
countryballs:
    ball 1: url
    ball 2: url again

ball_to_emoji:
  ball 1: emoji
  ball 2: emoji again

# i recommend reading the README inside this folder
# note, it doesnt need the ID, it needs the ACTUAL emoji id (something like <:full_rat:1205271877245730878>), you can get it by doing \:emoji_name: please note that it is CasE SensItivE
```
The file itself is mostly empty and won't work unless you provide the file your **emoji ID**, **collectible name** and **image URL**.

```yml
countryballs:
    full rat: https://bigrat.monster/media/perfect.png
#   ball 2: url again

ball_to_emoji:
    full rat: <:full_rat:1205271877245730878>
#   ball 2: emoji again

# i recommend reading the README inside this folder
# note, it doesnt need the ID, it needs the ACTUAL emoji id (something like <:full_rat:1205271877245730878>), you can get it by doing \:emoji_name: please note that it is CasE SensItivE
```
The codeblock above shows that we have "removed" the `ball 2` collectible. This is because we don't want to spawn a collectible that **isn't** valid.

We also provided the file our **emoji ID**, **collectible name**, and **image URL**. Currently, the URL is used as the spawn image for your recently added collectible, `full rat`.

### What Does This Do?
This section is for seeing what X thing does.
1. countryballs
   - `ball 1`
     - This is where you place the name of your collectible. E.G: `full rat`
   - `url`
     - This is where you place the link to your image. You can use tools like [Imgur Uploader](https://img.doerig.dev/) to upload your image to Imgur to then use it for your bot. E.G: `https://i.imgur.com/TYpykXq.jpg`
   - Unlike the old `dex.py`, this one doesn't need the `,` to have multiple collectibles.
2. ball_to_emoji
   - `ball 1`
     - The collectible that will have the emoji. The collectible must be added in `countryballs`. E.G:   `full rat`
   - `emoji`
     - The emoji to be used in `/completion`. Get your emoji ID by sending this to a discord channel: `\:the_name_of_your_emoji:` then copy the text. It will look something like `<:the_name_of_your_emoji:1234567890>`, copy that and paste it.

## configured-channels.yml
The name should explain itself. But basically; this is where the spawn channels are stored.

The format is something like this:
```yml
Guild ID: Channel ID
Guild ID: Channel ID
``` 

## rarities.yml
In this file you can set the rarities for your [collectibles](README.md/#collectiblesyml).

The codeblock below includes the default file.
```yml
rarities:
  ball 1: rarity # for example, 1!
  ball 2: rarity again # for example, 2!
```
In this one, you'll do what you did in [collecitbles.yml](README.md/#collectiblesyml) but with rarities instead of emoji IDs or URLs you'll use a number, E.G:
```yml
rarities:
  full rat: 1 # for example, 1!
#  ball 2: rarity again # for example, 2!
```
You can see we commented `ball 2`, this is for the same reason as mentioned above.
> [!NOTE]
> The rarity is **NEEDS** to be a __just a number__, this means that you can't have stuff like:
> ```yml
> rarities:
>   full rat: 00000.1 # for example, 1!
> #  ball 2: rarity again # for example, 2!
>  ```
> If  you want something like that, you would probably do something like this:
> ```yml
> rarities:
>    full rat: 000001 # for example, 1!
> #   ball 2: rarity again # for example, 2!
> ```
## config.yml
The configuration file. Editing this file is **required**.

Here's the file: *(For previewing.)*
```yml
# Welcome to the config file. Please read the README.md file found at the ymls folder.

bot-token: "Your Token Here" # The bot token for your bot.
text-prefix: "b." # The prefix for text commands. They can be found at the README file mentioned above.

# Stuff that will be shown on /about.
about:
  description: "Collect balls on Discord. Made for people without Docker or PC." # Edits the first line of /about.
  github-link: "https://github.com/wascertified/dockerless-dex" # Only change this if you have a fork, this is not required and can be skipped.
  discord-invite: "https://discord.gg/RSdcTAn7FG" # Change to your discord server.

# Stuff that will be used on commands.
collectibles-name: "ball" # Don't add an "s" as the bot will already add the extra "s".
bot-name: "Dockerless-Dex" # The name of the dex.
players-group-cog-name: "balls" # No spaces, must be lowercase.

authorized-users:
  - USER ID HERE 
  
# For having multiple, just make sure it matches this look:
#  - 1234567890
#  - 1234567890
# Without the "#", though. The "#" must be ignored if you want multiple.

### NOTES ON AUTHORIZED USERS:
# Only give to people you trust.
# It will also give the user the permission of using the kill command (which turns off the bot)
# With great power comes great responsability.
```
> [!NOTE]
> The `bot-token` is required. You can find the the proccess of getting your token [here](https://invidious.drgns.space/watch?v=aI4OmIbkJH8).

### What Does This Do?
This section is for seeing what X thing does.
#### Main
1. bot-token
   - Tells `dex.py` the discord bot token so it can run it.
2. text-prefix
   - The prefix for text-based commands. Some of them include `giveball`, `spawnball`, and `reloadtree`.
     - `giveball {user id or mention} {valid collectable}` | Gives a ball to mentioned user.
     - `spawnball {valid collectable}`                     | The collectable is optional.
     - `reloadtree`                                        | Reloads trees. *(slash commands)*
     - `serverblacklist {server id} {reason}`              | Blacklists a server.
     - `serverblacklistremove {server id} {reason}`        | Removes the blacklist from a server.
     - `blacklist {user} {reason}`                         | Blacklists mentioned user.
     - `blacklist {user} {reason}`                         | Removes the blacklist from a user.
#### About Section
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
#### Owners Section
1. authorized-users
   - Users allowed to use the text commands.
     - `giveball {user id or mention} {valid collectable}` | Gives a ball to mentioned user.
     - `spawnball {valid collectable}`                     | The collectable is optional.
     - `reloadtree`                                        | Reloads trees. *(slash commands)*
     - `serverblacklist {server id} {reason}`              | Blacklists a server.
     - `serverblacklistremove {server id} {reason}`        | Removes the blacklist from a server.
     - `blacklist {user} {reason}`                         | Blacklists mentioned user.
     - `blacklist {user} {reason}`                         | Removes the blacklist from a user.
