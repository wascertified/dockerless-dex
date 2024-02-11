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

This is what it would look like if we were to add a "full_rat" ball.
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
 "perfect rat": "https://bigrat.monster/media/perfect.png"
# "ball name 2": "ball url 2"
# add more if you want, this is just an example.
}
```
> [!NOTE]
> An `,` is required after adding the first ball. E.G:
> 
> "ball name": "ball url"**,**
> "ball name2": "ball url2"
> 
> As you can see, the second line doesn't have the `,` like the first one.