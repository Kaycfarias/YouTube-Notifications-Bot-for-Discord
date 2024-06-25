import discord
import sqlite3

import assets.core


class dropdownChannel(discord.ui.Select):
    def __init__(self, classe_externa):
        self.classe_externa = classe_externa
        self.option = []
        conn = sqlite3.connect("youtube_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM youtube_channels")
        all_channels = cursor.fetchall()
        conn.commit()
        conn.close()
        super().__init__(placeholder="Editar canais", custom_id="edit_channel", options=self.option)
        if len(all_channels) > 0:
            for channel in all_channels:
                self.option.append(discord.SelectOption(label=channel[1], value=channel[0]))
        else:
            self.option.append(discord.SelectOption(label="VAZIO", value="VAZIO"))
            self.disabled = True

    async def callback(self, inter):
        conn = sqlite3.connect("youtube_data.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM youtube_channels WHERE channel_id = ?",
            (self.values[0],),
        )
        channel = cursor.fetchall()
        embed = discord.Embed(
            title=channel[0][1],
            description=f"ID:{channel[0][0]}\nÚltimo vídeo: {channel[0][2]}\nCanal de notificações: {channel[0][3]}",
            color=0xFF0000,
        )
        await inter.response.edit_message(
            embed=embed, view=assets.core.editView(self.values[0], self.classe_externa)
        )