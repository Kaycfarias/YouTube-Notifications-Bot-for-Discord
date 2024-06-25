import discord
import sqlite3


class youtubeEditModal(discord.ui.Modal):
    def __init__(self, ID):
        self.ID = ID
        conn = sqlite3.connect("youtube_data.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MAX(channel_name) FROM youtube_channels WHERE channel_id = ?",
            (self.ID,),
        )
        self.n = cursor.fetchall()
        cursor.execute(
            "SELECT MAX(latest_video_url) FROM youtube_channels WHERE channel_id = ?",
            (self.ID,),
        )
        self.u = cursor.fetchall()
        cursor.execute(
            "SELECT MAX(notifying_discord_channel) FROM youtube_channels WHERE channel_id = ?",
            (self.ID,),
        )
        self.c = cursor.fetchall()
        conn.commit()
        conn.close()
        super().__init__(title=f"Editar canal {self.n[0][0]}")
        self.nome = discord.ui.TextInput(
            label="Nome do canal do youtube", default=self.n[0][0], style=discord.TextStyle.short
        )
        self.url = discord.ui.TextInput(
            label="Penultimo e ultimo video.(Não mexa)", default=self.u[0][0], style=discord.TextStyle.short
        )
        self.ID_channel = discord.ui.TextInput(
            label="Id canal de notificações", default=self.c[0][0], style=discord.TextStyle.short
        )
        self.add_item(self.nome)
        self.add_item(self.url)
        self.add_item(self.ID_channel)

    async def on_submit(self, inter: discord.Interaction):
        conn = sqlite3.connect("youtube_data.db")
        cursor = conn.cursor()
        cursor.execute(
            """
        UPDATE youtube_channels
        SET channel_name = ?,
        latest_video_url = ?,
        notifying_discord_channel = ?
        WHERE channel_id = ?
            """,
            (self.nome.value, self.url.value, self.ID_channel.value, self.ID),
        )
        conn.commit()
        conn.close()
        embed = discord.Embed(
            title=self.nome.value,
            description=f"ID:{self.ID}\nÚltimo vídeo: {self.url.value}\nCanal de notificações: {self.ID_channel.value}",
            color=0xFF0000,
        )
        await inter.response.edit_message(embed=embed)