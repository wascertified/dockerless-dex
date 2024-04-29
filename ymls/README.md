# YMLS/ FOLDER
In this README markdown file I'll teach you some stuff about the YAMLs, so you're good to go once you decide if you want to selfhost.

## collectibles.yml
This YAML file is where you will add your collectables. Since you just cloned the repo *(or downloaded it)*, your file will probably look something like this:
```yml
countryballs:
    ball 1: url
#   big rat: https://bigrat.monster/media/perfect.png

ball_to_emoji:
    ball 1: emoji
#   big rat: <:bigrat:1227419022375649340>

catch_names:
  ball 1:
    - catch name 1
    - catch name 2
# big rat:
#   - big rat
#   - perfect rat
#   - awesome rat
#   - rat
#   - such rat much wow


#### NOTES: ####
# These texts that begin with '#' are comments, they are ignored by both Python and YAML. They are mostly used to explain something,
# And here I'm giving examples; If you don't know how to get your 'FULL' emoji ID, go to the README inside this folder.
# Please, make sure to do the correct syntax.
# Read the README inside the folder, as we highly recommend you to do so.
```
The commented out text *(those begginning with `#`)* are examples of how you add an spawn art, emoji, and catch names.

**Here's what everything does:**
* `countryballs:` - The start of the 'countryballs' list. **This is needed.**
  * `ball 1: url`
    * `ball 1` - The main collectible, this is case sensitive on the files. You may want to repeat it over at `catch_names:`. **This is needed.**
    * `:` - Separator so it is easier to read. **This is needed.**
    * `url` - Image URL. This will be the 'spawn-art' shown. **This is needed.**
* `ball_to_emoji` - The start of the 'ball_to_emoji' list. **This is needed.**
  * `ball 1: emoji`
    * `ball 1` - As mentioned, this is the main collectible and it must be the exact same as `ball 1` below `countryballs`. **This is needed.**
    * `:` - Separator.
    * `emoji` - The full ID of the emoji *(not `:emoji_name:`)*. **This is needed.**
      * To get the 'full ID' of the emoji, activate Developer Mode under `Settings > Advanced` in Discord. After doing so, go to the server where your emoji is in and send it:
        * ![img](https://i.imgur.com/6UlKUu5.png)
      * After doing so, edit the message by either pressing the `UP` key or clicking on the pencil while hovering over the message. Now, add a backslash *(`\`)* at the start of the message:
        * ![img](https://i.imgur.com/DltULv4.png)
      * And save it! After doing that, you will see something like this:
        * ![img](https://i.imgur.com/SubwfXh.png)
      * That is your full emoji ID, congrats!
      * **PLEASE NOTE THAT THE BOT MUST BE IN THE SERVER FOR IT TO WORK.**
* `catch_names` - The start of the 'catch_names' list. **This is needed.**
  * I'll work on this soon.

## configured-channels.yml
The name should explain itself. But basically; this is where the spawn channels are stored.

The format is something like this:
```yml
Guild ID: Channel ID
Guild ID: Channel ID
``` 

## rarities.yml
In this file you can set the rarities for your [collectibles](README.md/#collectiblesyml):
```yml
rarities:
  ball 1: 1
# big rat: 1

#### NOTES: ####
# These texts that begin with '#' are comments, they are ignored by both Python and YAML. They are mostly used to explain something.
# The comment above, 'big rat: 1' is an example on how to do so. the first entry ('big rat') is the collectible inside collectibles.yml,
# it must be the exact same as the one below 'countryballs:'. The number ('1') is the rarity. It can not be a floating number (e.g.: '1.5'),
# so watch out for that.
# Please also make sure to use the correct syntax.
# Read the README inside the folder, as we highly recommend you to do so.
```
I won't say much about this, as I believe the comment already does that.

## config.yml
The configuration file. Editing this file is **required**:

```yml
# Welcome to the config file. Please read the README.md file found at the ymls folder.

bot-token: "Your Token Here" # The bot token for your bot.
text-prefix: "b."            # The prefix for text commands. They can be found at the README file mentioned above.

# Stuff that will be shown on /about.
about:
  description: "Collect balls on Discord. Made for people without Docker or PC." # Edits the first line of /about.
  github-link: "https://github.com/wascertified/dockerless-dex"                  # Only change this if you have a fork, this is not required and can be skipped.
  discord-invite: "https://discord.gg/RSdcTAn7FG"                                # Change to your discord server.

# Stuff that will be used on commands.
collectibles-name: "ball"       # Don't add an "s" as the code will already add the extra "s".
bot-name: "Dockerless-Dex"      # The name of the dex.
players-group-cog-name: "balls" # No spaces, must be lowercase.

# Bot startup status configuration.
startup_status:
  activity_type: "watching"                # Options: playing, streaming, listening, watching
  activity_name: "Dockerless-Dex"          # Name of the activity.
  status: "dnd"                            # Options: online, idle, dnd, invisible
  stream_url: "http://twitch.tv/settings"  # Required if activity_type is streaming. If it is a YouTube link, it must be a Stream-type video.
```
> [!NOTE]
> The `bot-token` is required. You can find the the proccess of getting your token [here](https://invidious.drgns.space/watch?v=aI4OmIbkJH8).

### What Does This Do?
This section is for seeing what X thing does.
>[!WARNING]
>This header is outdated but I still believe it helps. I'll rewrite it some time soon, so watch out for that.

#### Main
1. bot-token
   - Tells `dex.py` the discord bot token so it can run it.
2. text-prefix
   - The prefix for text-based commands. Some of them include `giveball`, `spawnball`, and `reloadtree`.
     - `giveball {user id or mention} {valid collectible}` | Gives a ball to mentioned user.
     - `spawnball {valid collectible}`                     | The collectible is optional.
     - `reloadtree`                                        | Reloads trees. *(slash commands)*
     - `serverblacklist {server id} {reason}`              | Blacklists a server.
     - `serverblacklistremove {server id} {reason}`        | Removes the blacklist from a server.
     - `blacklist {user} {reason}`                         | Blacklists mentioned user.
     - `blacklist {user} {reason}`                         | Removes the blacklist from a user.
#### About Section
* `description`
  * The text that will be shown at the start of `/about`.
* `github-link`
  * Changes the github link present in `/about`. It is not required to edit this nor to make a fork.
* `discord-invite`
  * Changes the discord invite present in `/about`. Defaults to the support server, change if you have an official server.
#### Commands Section
1. collectibles-name
   * Changes the messages in the bot to refer to your collectables. E.G: You caught a new ball!
2. bot-name
   * Changes the messages in the bot to refer to your bot. E.G: Dockerless-Dex will start spawning balls in this channel. *(Not an actual message inside the bot, but you get the point.)*
3. players-group-cog-name
   * Changes the begginning of the commands for your bot. E.G: /balls_list *(Please note that it can only be lowercase and can't contain spaces.)*
