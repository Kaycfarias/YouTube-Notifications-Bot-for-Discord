import discord
import sqlite3

import assets.core

class editView(discord.ui.View):
    def __init__(self, ID, classe_externa):
        self.classe_externa = classe_externa
        self.ID = ID
        super().__init__()
        self.add_item(assets.core.dropdownChannel(self.classe_externa))

    @discord.ui.button(
        style=discord.ButtonStyle.grey,
        label="<",
        custom_id="Voltar",
    )
    async def voltar(self, inter, button):
        await inter.response.edit_message(
            embed=assets.core.embedVideos(), view=assets.core.youtubeView(self.classe_externa)
        )

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Editar",
        custom_id="editar",
    )
    async def edit(self, inter, button):
        await inter.response.send_modal(assets.core.youtubeEditModal(self.ID))

    @discord.ui.button(
        style=discord.ButtonStyle.red,
        label="Apagar",
        custom_id="Apagar",
    )
    async def clear(self, inter, button):
        conn = sqlite3.connect("youtube_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM youtube_channels WHERE channel_id = ?", (self.ID,))
        conn.commit()
        conn.close()
        await inter.response.edit_message(
            embed=assets.embedVideos(), view=assets.core.youtubeView(self.classe_externa)
        )