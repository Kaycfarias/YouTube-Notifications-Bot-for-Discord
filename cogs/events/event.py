import sqlite3

import discord
from discord.ext import commands


class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        self.bot.synced = True
        activity = discord.Activity(type=discord.ActivityType.watching, name="YouTube")
        await self.bot.change_presence(activity=activity)
        print(
            f"\nEntramos como: {self.bot.user.name} - {self.bot.user.id}\nVersão: {discord.__version__}:"
        )
        print(f"Logado e iniciado com sucesso...!\n")
        conn = sqlite3.connect("youtube_data.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS youtube_channels (
            channel_id TEXT PRIMARY KEY,
            channel_name,
            latest_video_url,
            notifying_discord_channel
            )
            """
        )
        conn.commit()
        conn.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(event(bot))
