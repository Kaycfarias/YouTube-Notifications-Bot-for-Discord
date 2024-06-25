import discord
import sqlite3
import aiohttp
import re

from assets.core import embedVideos
from assets.core import youtubeView
from discord import app_commands
from discord.ext import commands, tasks


class yt(commands.Cog):
    @tasks.loop(seconds=20)
    async def checkforvideos(self):
        conn = sqlite3.connect("youtube_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM youtube_channels")
        all_channels = cursor.fetchall()
        for youtube_channel in all_channels:
            try:
                async with aiohttp.ClientSession() as session, session.get(
                    f"https://www.youtube.com/channel/{youtube_channel[0]}/videos"
                ) as resp:
                    html = await resp.text()

                    video_id = re.search('(?<="videoId":").*?(?=")', html)
                    if video_id:
                        latest_video_url = f"https://youtu.be/{video_id.group()}"
                    else:
                        continue

            except aiohttp.ClientError:
                    continue
                
            if latest_video_url not in youtube_channel[2]:
                    penu, last = youtube_channel[2].split(",", 2)
                    cursor.execute(
                        """UPDATE youtube_channels SET latest_video_url = ? WHERE channel_id = ? """,
                        (f"{last}, {latest_video_url}", youtube_channel[0]),
                    )
                    conn.commit()

                    await self.bot.get_channel(int(youtube_channel[3])).send(
                        f"Saiu vídeo novo no canal {youtube_channel[1]}!!!\nAssistir Agora: [NOVO VIDEO]({latest_video_url})")
                    
    def __init__(self, bot):
        self.bot = bot
        self.checkforvideos.start()

    @app_commands.guild_only()
    @app_commands.command(
        name="youtube", description="Veja e edite os canais na lista de notificação"
    )
    async def status(self, i:discord.Interaction):
        if i.user.guild_permissions.administrator:
            embed = embedVideos()
            await i.response.send_message(embed=embed, view=youtubeView(self), ephemeral=True)
        else:
            return await i.response.send_message("somente ADMS", ephemeral=True, delete_after=7)

async def setup(bot: commands.Bot):
    await bot.add_cog(yt(bot))