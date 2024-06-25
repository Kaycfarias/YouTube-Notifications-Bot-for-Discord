import discord
import sqlite3

import assets.core

class youtubeViewModal(discord.ui.Modal):
    def __init__(self, cls_ext):
        self.cls_ext = cls_ext
        super().__init__(title="Novo canal")
        self.id_yt = discord.ui.TextInput(
            label="Id do canal youtube", style=discord.TextStyle.short
        )
        self.nome = discord.ui.TextInput(label="Nome do canal do youtube", style=discord.TextStyle.short)
        self.ID_channel = discord.ui.TextInput(
            label="Id canal de notificações", style=discord.TextStyle.short
        )
        self.add_item(self.id_yt)
        self.add_item(self.nome)
        self.add_item(self.ID_channel)

    async def on_submit(self, inter: discord.Interaction):
        conn = sqlite3.connect("youtube_data.db")
        cursor = conn.cursor()
        new_channel = (
            self.id_yt.value,
            self.nome.value,
            "https://youtu.be/abc123, https://youtu.be/abc123",
            self.ID_channel.value,
        )
        cursor.execute(
            """ INSERT INTO youtube_channels (channel_id, channel_name, latest_video_url, notifying_discord_channel) VALUES (?, ?, ?, ?) """,
            new_channel,
        )
        conn.commit()
        conn.close()
        embed = assets.core.embedVideos()
        await inter.response.edit_message(embed=embed, view=assets.core.youtubeView(self.cls_ext))