# Dockerless-Dex
Dockerless-Dex *(in a simplified way)* is a way to make dex's without a PC or Docker.

Below are the installation process for various systems, aswell as some other stuff you may also want to read.

## Linux Installation
1. First of all, install the needed packages. *(This heavily depends on your package manager; Here I'm using `pacman` as an example.)*
```sh
sudo pacman -S python python-pip git neovim nano
```
>[!NOTE]
>`git`, `nano`, and `neovim` are __optional__ as `git` will be used for cloning the repository. `nano` and `neovim` are used for editing text through the terminal; you will probably have those three already installed, depending on your distribution or previous actions.

2. After installing the packages, clone the repository with `git` or download it manually from [here](https://github.com/wascertified/dockerless-dex/releases).
```sh
cd "$HOME" ; git clone https://github.com/wascertified/dockerless-dex ; cd "$HOME/dockerless-dex"
# The command above will send you to your home directory then clone the GitHub repository then send you inside the folder. The ";" will run the command once the previous one finishes.
```
3. Once you clone the GitHub repository, you can edit the `config.yml` file with your prefered text editor:
```sh
nvim config.yml # Press "i" to go into instert mode, to exit press ESC to exit insert mode; write ":wq" to exit. (write, quit)

# Or:
nano config.yml # To exit, press CTRL + X.

# Once you're inside the file, edit it as it is required for your bot to turn on.
```

4. Now you can make a VENV *(Virtual ENViroment)* with python to install the dependencies.
```sh
python -m venv .venv # Creates the .venv folder.

source ".venv/bin/activate" # Activates the .venv folder. This will only work if you're using BASH. To know which one you're using, run "which $SHELL" in your terminal.

pip install discord.py pyyaml requests # Installs dependencies.
```
>[!TIP]
>Your package manager may contain the dependencies. E.G.:
>```sh
>yay -S python-yaml python-discord-py python-requests
>```

>[!NOTE]
>Creating the VENV isn't required but I still \*personally\* recommend **you** to make it.

5. Now that you got everything ready, make sure that:
   - You have everything under Bot -> Priviliged Gateway Intents ![](https://cdn.discordapp.com/attachments/1204312915432439840/1206397619564314624/image.png?ex=65dbdc56&is=65c96756&hm=e4ddfb943bde269418170012b27f139380becd18c4e32b929e7d1a023aac16d2&)
   - Have a correct invite link. ![](https://cdn.discordapp.com/attachments/1204312915432439840/1206397813412335626/image.png?ex=65dbdc84&is=65c96784&hm=6979555fce3770d1f2c4aff7aae8925a8eefee8fa63b88c5e57b42833628939e&)
     - You get that all that done [here](https://discord.com/developers).

7. You can find some documentaion on how to add collectables [here](https://github.com/wascertified/dockerless-dex/tree/main/ymls). The link mentioned also works as a guide for the YML files.

8. If everything you did turned out well, you can *finally* run the bot.

```sh
python dex.py # Believing you're still in the dockerless-dex/ folder.
```

## Windows Installation
1. First of all, download python from [here](https://www.python.org/downloads/) or the microsoft store.
2. Download git from [here](https://git-scm.com/downloads) **(OPTIONAL)**
   - `git clone https://github.com/wascertified/dockerless-dex.git`
   - If you don't want to use git, you can download the repository manually from [here](https://github.com/wascertified/dockerless-dex/releases).
3. After cloning *(or downloading the zip from the link provided)*, go to where you cloned the repository *(usually your profile folder)* and open the `config.yml` file with your favorite text editor.
4. Install the dependencies with `pip`.
   - `pip install discord.py pyyaml asyncio requests` 
5. Now that you got everything ready, make sure that:
   - You have everything under Bot -> Priviliged Gateway Intents ![](https://cdn.discordapp.com/attachments/1204312915432439840/1206397619564314624/image.png?ex=65dbdc56&is=65c96756&hm=e4ddfb943bde269418170012b27f139380becd18c4e32b929e7d1a023aac16d2&)
   - Have a correct invite link. ![](https://cdn.discordapp.com/attachments/1204312915432439840/1206397813412335626/image.png?ex=65dbdc84&is=65c96784&hm=6979555fce3770d1f2c4aff7aae8925a8eefee8fa63b88c5e57b42833628939e&)
     - You get that all that done [here](https://discord.com/developers).
6. You can find some documentaion on how to add collectables [here](https://github.com/wascertified/dockerless-dex/tree/main/ymls). The link mentioned also works as a guide for the YML files.
7. And you're done! Now you can run the bot if you've done everything correctly.
   - `python dex.py`

### Other Stuff
Found an issue? Got a question? Something just didn't work?

**[Join the support discord server](https://discord.gg/RSdcTAn7FG)**!

