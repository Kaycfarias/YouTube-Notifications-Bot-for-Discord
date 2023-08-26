import re
import sqlite3

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks


def embedvideos():
    conn = sqlite3.connect("youtube_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM youtube_channels")
    all_channels = cursor.fetchall()
    embed = discord.Embed(title="Canais do youtube", color=0xFF0000)
    for channel in all_channels:
        embed.add_field(
            name=channel[1],
            value=f"ID: {channel[0]}\nÚltimo vídeo: {channel[2]}\nCanal de notificações: {channel[3]}",
            inline=False,
        )
    conn.commit()
    conn.close()
    return embed


class YouTubeEditModal(discord.ui.Modal):
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


class YouTubeViewModal(discord.ui.Modal):
    def __init__(self, classe_externa):
        self.classe_externa = classe_externa
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
        embed = embedvideos()
        await inter.response.edit_message(embed=embed, view=YouTubeView(self.classe_externa))


class DropDownC(discord.ui.Select):
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
            embed=embed, view=EditView(self.values[0], self.classe_externa)
        )


class EditView(discord.ui.View):
    def __init__(self, ID, classe_externa):
        self.classe_externa = classe_externa
        self.ID = ID
        super().__init__()
        self.add_item(DropDownC(self.classe_externa))

    @discord.ui.button(
        style=discord.ButtonStyle.grey,
        label="<",
        custom_id="Voltar",
    )
    async def voltar(self, inter, button):
        await inter.response.edit_message(
            embed=embedvideos(), view=YouTubeView(self.classe_externa)
        )

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Editar",
        custom_id="editar",
    )
    async def edit(self, inter, button):
        await inter.response.send_modal(YouTubeEditModal(self.ID))

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
            embed=embedvideos(), view=YouTubeView(self.classe_externa)
        )


class YouTubeView(discord.ui.View):
    def __init__(self, classe_externa):
        self.classe_externa = classe_externa
        self.bot = self.classe_externa.bot
        super().__init__()
        self.add_item(DropDownC(self.classe_externa))
        if self.classe_externa.checkforvideos.is_running():
            for child in self.children:
                if child.custom_id == "start/stop":
                    child.label, child.style = "PARAR", discord.ButtonStyle.red

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="INICIAR",
        custom_id="start/stop",
    )
    async def s_p(self, inter, button):
        if self.classe_externa.checkforvideos.is_running():
            self.classe_externa.checkforvideos.stop()
            button.label = "INICIAR"
            button.style = discord.ButtonStyle.green
            await inter.response.edit_message(view=self)
        else:
            self.classe_externa.checkforvideos.start()
            button.label = "INICIAR"
            button.style = discord.ButtonStyle.red
            await inter.response.edit_message(view=self)

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        label="Adicionar Canal do YouTube",
        custom_id="add_channel",
    )
    async def edd_channel(self, inter, button):
        await inter.response.send_modal(YouTubeViewModal(self.classe_externa))


class yt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @app_commands.guild_only()
    @app_commands.command(
        name="youtube", description="Veja e edite os canais na lista de notificação"
    )
    async def status(self, i:discord.Interaction):
        if i.user.guild_permissions.administrator:
            embed = embedvideos()
            await i.response.send_message(embed=embed, view=YouTubeView(self), ephemeral=True)
        else:
            return await i.response.send_message("somente ADMS", ephemeral=True, delete_after=7)

    def cog_unload(self):
        self.checkforvideos.cancel()
    def cog_load(self):
        self.checkforvideos.start()

async def setup(bot: commands.Bot):
    await bot.add_cog(yt(bot))