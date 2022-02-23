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
import requests
from bs4 import BeautifulSoup
import random
listelien=[]
urllol="https://lolprofile.net/fr/summoner/euw/"
urlcg = "https://www.topachat.com/pages/produits_cat_est_micro_puis_rubrique_est_wgfx_pcie.html"

client = commands.Bot(command_prefix=';;')

players = {}

@client.event
async def on_ready():
    activity = discord.Game(name=";;aide <-- pour liste des commandes")
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
    embeb.add_field(name=";;profil 'joueur'", value="permet d'obtenir le profil d'un joueur de lol", inline=True)
    embeb.add_field(name=";;rank 'joueur'", value="permet d'obtenir le rank d'un joueur de lol", inline=True)
    await ctx.send(embed=embeb)

@client.command()
async def profil(ctx, *, profil):
    profil2=profil
    profil=profil.split(" ")
    new_profil = ""
    for i in profil :
        new_profil = new_profil + i + "%20"
    url2= urllol + new_profil
    reponse = requests.get(url2)
    soup = BeautifulSoup(reponse.text)
    region= soup.find("span", {"class": 'region'})
    level= soup.find("div", {"class": 's-icon dhide'})
    embed4=discord.Embed(title=profil2, color=discord.Color.blue())
    imgprofil=soup.find("img", {"width": '60'}).attrs.get("src")
    embed4.add_field(name="Level", value=level.text, inline=True)
    embed4.set_footer(text=region.text)
    embed4.set_thumbnail(url=imgprofil)
    await ctx.send(embed=embed4)

@client.command()
async def gay(ctx, *, user):
    
    gayniv=random.randint(0,100)
    gayniv=str(gayniv)
    await ctx.send(user+" est gay a "+gayniv+"%")

@client.command()
async def couple(ctx, user1, user2):
    
    gayniv1=random.randint(0,100)
    gayniv1=str(gayniv1)
    await ctx.send(user1+" a "+gayniv1+"% de chance d'étre en couple avec "+user2)

@client.command()
async def CG(ctx):
    reponse = requests.get(urlcg)
    print(reponse)
    soup = BeautifulSoup(reponse.text)
    cg = soup.find("a", {"class": "tacenter"}).attrs.get("href")
    lien = "https://www.topachat.com/"+cg
    reponse2 = requests.get(lien)
    soup1 = BeautifulSoup(reponse2.text)
    cg2 = soup1.find("h1", {"class": "fn"})
    cg2 = cg2.text
    cg2image = soup1.find("img", {"class": "main-image"}).attrs.get("src")
    prix = soup1.find("span", {"class": "priceFinal fp44"}).attrs.get("content")
    embeb5=discord.Embed(title="Bon plan carte graphique du jour : \n"+"`"+cg2+"`",url=lien, color=discord.Color.blue())
    embeb5.add_field(name="Prix : \n", value="**"+prix+" €"+"**", inline=True)
    embeb5.set_image(url="https:"+cg2image)
    embeb5.set_footer(text="source : TopAchat")
    await ctx.send(embed=embeb5)

@client.command()
async def rank(ctx, *, profil):
    profil2=profil
    profil=profil.split(" ")
    new_profil = ""
    for i in profil :
        new_profil = new_profil + i + "%20"
    url2= urllol + new_profil
    reponse = requests.get(url2)
    soup = BeautifulSoup(reponse.text)
    elo=soup.find("span", {"class": 'tier'})
    lp=soup.find("span", {"class": 'lp'})
    win= soup.find("span", {"class": 'win-txt'})
    lose= soup.find("span", {"class": 'lose-txt'})
    embed3=discord.Embed(title=profil2, color=discord.Color.blue())
    embed3.add_field(name="Rank", value=elo.text+"   "+lp.text, inline=True)
    img=soup.find("img", {"width": '110'}).attrs.get("src")
    embed3.add_field(name="Win", value=win.text, inline=True)
    embed3.add_field(name="Lose", value=lose.text, inline=True)
    embed3.set_thumbnail(url=img)
    
    await ctx.send(embed=embed3)
    

@client.command()
async def play(ctx, *, url):
    
    if (url.startswith('https')):
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
            print(URL)
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
            listelien.clear()
    # check if the bot is already playing
        else:
            listelien.append(url)
            listelien.append(url)
            await ctx.send("added to queue "+'**'+url+'**')
            return
            return
    
    else:
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
                info = ydl.extract_info("ytsearch:"+url, download=False)
            URL = info['entries'][0]['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            #créer un embeb
            ydl_opts = {}
            url2="https://www.youtube.com/watch?v="+info['entries'][0]['id']
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(url2, download=False) 
            
            print(url2)
            embed=discord.Embed(title="Playing :", url=url2, description=meta['title'], color=discord.Color.blue())
            url_data = urlparse(url2)
            image = "https://img.youtube.com/vi/"+url_data.query[2:13]+"/maxresdefault.jpg"
            embed.set_thumbnail(url=image)
            embed.add_field(name="Vues", value=meta['view_count'], inline=True)
            embed.add_field(name="Likes", value=meta['like_count'], inline=True)
            embed.add_field(name="Durée", value=str(meta['duration'])+" secondes", inline=True)
            embed.add_field(name="Chaîne", value=(meta['uploader']), inline=True)
            embed.set_footer(text=url2)
            await ctx.send(embed=embed)
            embed1=discord.Embed(title="Description :", url=url2, description=meta['description'], color=discord.Color.blue())
            await ctx.send(embed=embed1)
            listelien.clear()


    # check if the bot is already playing
        else:
            listelien.append(url)
            await ctx.send("added to queue "+'**'+url+'**')
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

@client.command()
async def skip(ctx):
    
    voice = get(client.voice_clients, guild=ctx.guild)
    
    if voice.is_playing():
        voice.stop()
        await ctx.send('Skipping')
    url=listelien[0]
    if (url.startswith('https')):
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
            print(URL)
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
            listelien.clear()
    # check if the bot is already playing
        else:
            listelien.append(url)
            await ctx.send("added to queue "+'**'+url+'**')
            return
    
    else:
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
                info = ydl.extract_info("ytsearch:"+url, download=False)
            URL = info['entries'][0]['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            #créer un embeb
            ydl_opts = {}
            url2="https://www.youtube.com/watch?v="+info['entries'][0]['id']
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                meta = ydl.extract_info(url2, download=False) 
            
            print(url2)
            embed=discord.Embed(title="Playing :", url=url2, description=meta['title'], color=discord.Color.blue())
            url_data = urlparse(url2)
            image = "https://img.youtube.com/vi/"+url_data.query[2:13]+"/maxresdefault.jpg"
            embed.set_thumbnail(url=image)
            embed.add_field(name="Vues", value=meta['view_count'], inline=True)
            embed.add_field(name="Likes", value=meta['like_count'], inline=True)
            embed.add_field(name="Durée", value=str(meta['duration'])+" secondes", inline=True)
            embed.add_field(name="Chaîne", value=(meta['uploader']), inline=True)
            embed.set_footer(text=url2)
            await ctx.send(embed=embed)
            embed1=discord.Embed(title="Description :", url=url2, description=meta['description'], color=discord.Color.blue())
            await ctx.send(embed=embed1)
            listelien.clear()


    # check if the bot is already playing
        else:
            listelien.append(url)
            await ctx.send("added to queue "+'**'+url+'**')
            return

    


# command to clear channel messages
@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")




client.run('insert your token here')