import discord
import sqlite3

def embedVideos():
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