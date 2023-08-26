import os
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("config.env")

TOKEN_BOT = os.getenv("TOKEN_BOT")


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
        self.run(TOKEN_BOT)

    async def setup_hook(self):
        diretorio = os.listdir("./cogs")
        print("Cogs/")
        for f in diretorio:
            if f.endswith(".py"):
                try:
                    await self.load_extension("cogs." + f[:-3])
                    if diretorio.index(f) < len(diretorio) - 1:
                        print(f"├── {f}")
                    else:
                        print(f"└── {f}")
                except Exception:
                    print(f"Falha ao carregar: {f}")
                    traceback.print_exc()


MyBot()
