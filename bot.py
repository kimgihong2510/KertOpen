import asyncio
import discord
import pygame

client = discord.Client()

token='ODU1ODY2Mjc5MDA0ODY0NTcz.YM4tlg.xVVel6K8UvSefaOQzipDKGJq0KI'

@client.event
async def on_ready():
    print("다음으로 로그인합니다.")
    print(client.user.name)
    print(client.user.id)
    print("=============")

@client.event
async def on_message(message):
    if message.author.bot:
        return None

    status=1;

    if message.content == '?컬열?':
        if status:
            await message.channel.send('컬방 열려있어요')
        else:
            await message.channel.send('컬방 닫혀있어요')
    
    if message.content == '?열려라참깨':
        if status:
            await message.channel.send('띵동')
            pygame.mixer.init()
            pygame.mixer.music.load("bell.mp3")
            pygame.mixer.music.play()

        else:
            await message.channel.send('컬방 닫혀있어요') 

client.run(token)

