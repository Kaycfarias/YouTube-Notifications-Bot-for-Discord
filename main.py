from dotenv import dotenv_values

import discord
from discord.ext import commands

from assets.cogsloader import cogsLoader

config =  dotenv_values(".env")

TOKEN = config["TOKEN"]


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            case_insensitive=True,
            command_prefix="yt",
            intents=discord.Intents(
                members=True, messages=True, message_content=True, guild_messages=True, guilds=True
            ),
            help_command=None,
        )
        self.synced = False
        self.run(TOKEN)

    async def setup_hook(self):
        await cogsLoader(self)

MyBot()
