from __future__ import unicode_literals
import discord
import os
from discord import guild
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from discord_slash import SlashCommand, SlashContext
from youtube_dl import YoutubeDL
from urllib.parse import urlparse
from discord_slash.utils.manage_commands import create_choice, create_option
import youtube_dl


client = commands.Bot(command_prefix=';;')

players = {}

@client.event
async def on_ready():
    activity = discord.Game(name="Porn hub")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready")

@client.event
async def on_message_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
           await ctx.send("Unknown command")

# command to play sound from a youtube URL

@client.command()
async def aide(ctx):
    embeb=discord.Embed(title="Liste des commandes :", color=discord.Color.blue())
    embeb.add_field(name=";;play 'lien youtube'", value="Permet de jouer une video youtube", inline=True)
    embeb.add_field(name=";;pause", value="Met la musique joué en pause", inline=True)
    embeb.add_field(name=";;resume", value="Resume la musique joué", inline=True)
    embeb.add_field(name=";;stop", value="arrete la musique", inline=True)
    embeb.add_field(name=";;clear 'nombre'", value="permet de suprimer un nombre de message dans le chat", inline=True)
    await ctx.send(embed=embeb)

@client.command()
async def profil(ctx, profil):
    profil1="https://euw.op.gg/summoner/userName="+profil
    embed2=discord.Embed(title="Profil de "+profil+" sur Op.gg", url=profil1, color=discord.Color.blue())
    await ctx.send(embed=embed2)




@client.command()
async def play(ctx, url):
    
    #channel = le message, l'auteur, le channel vocal
    channel = ctx.message.author.voice.channel
    #voice = get voice client
    voice = get(client.voice_clients, guild=ctx.guild)
    #si le bot est deja dans un salon, changer de salon, else se connecter
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        #créer un embeb
        ydl_opts = {}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
               meta = ydl.extract_info(url, download=False) 

        print((meta['title']))
        embed=discord.Embed(title="Playing :", url=url, description=meta['title'], color=discord.Color.blue())
        url_data = urlparse(url)
        image = "https://img.youtube.com/vi/"+url_data.query[2:13]+"/maxresdefault.jpg"
        embed.set_thumbnail(url=image)
        embed.add_field(name="Vues", value=meta['view_count'], inline=True)
        embed.add_field(name="Likes", value=meta['like_count'], inline=True)
        embed.add_field(name="Durée", value=str(meta['duration'])+" secondes", inline=True)
        embed.add_field(name="Chaîne", value=(meta['uploader']), inline=True)
        embed.set_footer(text=url)
        await ctx.send(embed=embed)
        embed1=discord.Embed(title="Description :", url=url, description=meta['description'], color=discord.Color.blue())
        await ctx.send(embed=embed1)
# check if the bot is already playing
    else:
        await ctx.send("Bot is already playing")
        return

# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')
        

# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Stopping...')


# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")




client.run('OTI2MTI1Mjc2NjQyMDMzNzQ2.Yc3HYA.5sO2vkTVWeMNPYPJYlZ1KN4Y-gE')