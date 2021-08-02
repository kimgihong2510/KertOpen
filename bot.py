import asyncio
import time
import datetime
from pytz import timezone
from discord.ext import tasks
import discord
import light_sensor as update
import os
from gtts import gTTS

client = discord.Client()

forbidend=datetime.datetime.now(timezone('Asia/Seoul'))
status=update.Openornot()

token='ODU1ODY2Mjc5MDA0ODY0NTcz.YM4tlg.sdyBX-ggQThrEn0ziWcaQ2ApXRI'

forbidenchannels=[546610833824940042, 699572422734643261, 855787966945034290, 572759629029834772]

forbiddencommands=['sudo', 'sh', 'rm', 'fork', 'config', 'host', 'super']
sudocommands=['reboot']

def main():
    @tasks.loop(seconds=5)
    async def statusupdate():
        global status
        if datetime.datetime.now(timezone('Asia/Seoul')) > forbidend:
            status=update.Openornot()

        if status == 0 :        
            client.change_presence(status=discord.Status.idle)
        elif status == 1 :
            client.change_presence(status=discord.Status.online)
        elif status == 2 :
            client.change_presence(status=discord.Status.dnd)

    @client.event
    async def on_ready():
        statusupdate.start()
        print("시작합니다")


    @client.event
    async def on_message(message):
        if message.author.bot:
            return None

        if message.channel.id in forbidenchannels:
            return None

        global forbidend
        global status

        if datetime.datetime.now(timezone('Asia/Seoul')) > forbidend:
            status=update.Openornot()

        #closed 0, opened 1, forbidden 2
            
        if message.content == '?help':
            await message.channel.send("?출입금지[분] (어드민 권한 필요)\n?열렸나요\n?열어주세요\n?공지 [내용]")

        if message.content[0:4] == '?cmd':
            cmd = message.content[5:]
            res = message.author.display_name + " $ "
            is_safe = True

            for c in forbiddencommands:
                if c in cmd:
                    is_safe = False
                    break

            if is_safe:
                if cmd in sudocommands:
                    cmd = "sudo " + cmd
                res += os.popen(cmd).read()
            else:
                res += "no hack."
            
            await message.channel.send(res)

        if message.content[0:5] == '?출입금지':
            if message.author.guild_permissions.administrator==True:
               try:
                   forbidtime=int(message.content[5:])
                   
                   if forbidtime < 0 : 
                       await message.channel.send("입력 형태가 올바르지 않습니다")
                       return None

                   forbidend=datetime.datetime.now(timezone('Asia/Seoul'))+datetime.timedelta(minutes=forbidtime)
                   forbidendstring=str(forbidend)
                   await message.channel.send(forbidendstring[0:19] + "까지 출입금지입니다")
                   status=2
               except:
                   await message.channel.send("입력 형태가 올바르지 않습니다")
            else :
                await message.channel.send("권한이 없습니다")
        

        if message.content == '?열렸나요':
            if status==1:
                await message.channel.send('열렸습니다')
            elif status==2:
                forbidendstring=str(forbidend)
                await message.channel.send(forbidendstring[0:19] + "까지 출입금지입니다")
            else:
                await message.channel.send('닫혔습니다')
    
        
        if message.content == '?열어주세요':
            if status==1:
                await message.channel.send('띵동')
                try:
                    result = ''.join([i for i in message.author.display_name if not (i.isdigit() or i=='_')])

                    tts = gTTS(text=(result + "님께서 왔습니다"), lang='ko')
                    os.system("mplayer bell.mp3")
                    tts.save("hell.mp3")
                    os.system("mplayer hell.mp3")
                except:
                    await message.channel.send('초인종이 작동을 안해요 ㅠㅠ 다른 방법을 이용해주세요')

            elif status==2:
                forbidendstring=str(forbidend)
                await message.channel.send(forbidendstring[0:19] + "까지 출입금지입니다")

            else:
                await message.channel.send('컬방이 닫혀있습니다')

        if message.content[:3] == '?공지':
            broadcast = message.content[4:]
            if status==1:
                await message.channel.send(broadcast + '와 같이 보냈습니다')
                try:
                    result = ''.join([i for i in message.author.display_name if not (i.isdigit() or i=='_')])
                    tts = gTTS(text=result + " 님께서 알립니다. " + broadcast, lang='ko')
                    tts.save("hell.mp3")
                    os.system("mplayer hell.mp3")
                except:
                    await message.channel.send('초인종이 작동을 안해요 ㅠㅠ 다른 방법을 이용해주세요')

            elif status==2:
                forbidendstring=str(forbidend)
                await message.channel.send(forbidendstring[0:19] + "까지 출입금지입니다")

            else:
                await message.channel.send('컬방이 닫혀있습니다') 

    client.run(token)


try:
    main()
except KeyboardInterrupt:
    pass
print("종료합니다") 
