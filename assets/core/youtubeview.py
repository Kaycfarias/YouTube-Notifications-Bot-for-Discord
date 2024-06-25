import discord
import assets.core


class youtubeView(discord.ui.View):
    def __init__(self, cls_ext):
        self.bot = cls_ext.bot
        self.cls_ext = cls_ext
        super().__init__()
        self.add_item(assets.core.dropdownChannel(self.cls_ext))
        if self.cls_ext.checkforvideos.is_running():
            for child in self.children:
                if child.custom_id == "start/stop":
                    child.label, child.style = "PARAR", discord.ButtonStyle.red

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="INICIAR",
        custom_id="start/stop",
    )
    async def s_p(self, inter, button):
        if self.cls_ext.checkforvideos.is_running():
            self.cls_ext.checkforvideos.stop()
            button.label = "INICIAR"
            button.style = discord.ButtonStyle.green
            await inter.response.edit_message(view=youtubeView(self.cls_ext))
        else:
            self.cls_ext.checkforvideos.start()
            button.label = "INICIAR"
            button.style = discord.ButtonStyle.red
            await inter.response.edit_message(view=youtubeView(self.cls_ext))

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        label="Adicionar Canal do YouTube",
        custom_id="add_channel",
    )
    async def edd_channel(self, inter, button):
        await inter.response.send_modal(assets.core.youtubeViewModal(self.cls_ext))