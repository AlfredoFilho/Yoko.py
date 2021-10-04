#!/bin/bash/python3
#coding: utf-8

import os
import random
import discord
import requests
from PIL import Image
from pathlib import Path
from discord_components import Button, ButtonStyle


async def tojpgCommand(ctx):

    if not ctx.message.attachments:
        await ctx.send("Não encontrei um arquivo na sua mensagem.\nEnvie uma imagem **PNG** juntamente com o comando **-tojpg**.")

    else:

        pathToImageJPG = "tmp/imageJPG-" + str(random.randint(100000, 1000000)) + ".jpg"
        pathToImagePNG = "tmp/imagePNG-" + str(random.randint(100000, 1000000)) + ".png"
        urlImageFromDiscord = ctx.message.attachments[-1].url

        if '.png' not in urlImageFromDiscord:
            await ctx.send('''
A extensão da sua imagem não é **.png**
Lembrete: -tojpg converte PNG para JPG
''')
        else:
            try:
                # os.system("wget -q -O {0} {1}".format(pathToImagePNG, urlImageFromDiscord))
                with open(pathToImagePNG, 'wb') as f:
                    f.write(requests.get(urlImageFromDiscord).content)

            except:
                await ctx.send('''
**Não consegui salvar sua imagem para converter :(** .
**Possível motivo:**
- Instabilidade no Discord: Tente novamente mais tarde.
''')
                return
            try:
                # Convert image
                im = Image.open(pathToImagePNG)
                rgb_im = im.convert('RGB')
                rgb_im.save(pathToImageJPG)
            
            except:
                
                await ctx.send("Não consegui converter esse arquivo para JPG.\nIsso é realmente uma imagem? :thinking:")
                deleteImagesLocal(pathToImageJPG, pathToImagePNG)
                return

            # Send image to channel
            f = discord.File(pathToImageJPG, filename="imageJPG.jpg")
            embedImagem = discord.Embed(
                title='Imagem em JPG',
                description='_Os comandos podem ser usados juntos com o envio do arquivo._',
                colour=discord.Colour(0xFF007F)
            )

            embedImagem.set_image(url='attachment://imageJPG.jpg')
            messageWithFile = await ctx.reply(file=f, embed=embedImagem)

            # Send button with URL of image
            await ctx.send(content="_ _", components=[
                Button(style=ButtonStyle.URL,
                       url=f"{messageWithFile.embeds[0].image.url}",
                       label='Link')
            ])

            deleteImagesLocal(pathToImageJPG, pathToImagePNG)


def deleteImagesLocal(pathToImageJPG, pathToImagePNG):

    my_file = Path(pathToImageJPG)
    if my_file.is_file():
        os.remove(pathToImageJPG)
    
    my_file = Path(pathToImagePNG)
    if my_file.is_file():
        os.remove(pathToImagePNG)


async def topngCommand(ctx):

    if not ctx.message.attachments:
        await ctx.send("Não encontrei um arquivo na sua mensagem.\nEnvie uma imagem **JPG** juntamente com o comando **-topng**.")

    else:

        pathToImageJPG = "tmp/imageJPG-" + str(random.randint(100000, 1000000)) + ".jpg"
        pathToImagePNG = "tmp/imagePNG-" + str(random.randint(100000, 1000000)) + ".png"
        urlImageFromDiscord = ctx.message.attachments[-1].url

        if '.jpg' not in urlImageFromDiscord:
            await ctx.send('''
A extensão da sua imagem não é **.jpg**
Lembrete: -topng converte JPG para PNG
''')
        else:
            try:
                # os.system("wget -q -O {0} {1}".format(pathToImageJPG, urlImageFromDiscord))
                with open(pathToImageJPG, 'wb') as f:
                    f.write(requests.get(urlImageFromDiscord).content)

            except:
                await ctx.send('''
**Não consegui salvar sua imagem para converter :(** .
**Possível motivo:**
- Instabilidade no Discord: Tente novamente mais tarde.
''')
                return
            try:
                # Convert image
                im = Image.open(pathToImageJPG)
                im.save(pathToImagePNG, 'png')
            
            except:

                await ctx.send("Não consegui converter esse arquivo para PNG.\nIsso é realmente uma imagem? :thinking:")
                deleteImagesLocal(pathToImageJPG, pathToImagePNG)
                return

            sizeImage = int(os.stat(pathToImagePNG).st_size)

            if sizeImage > 8000000:
                await ctx.channel.send('**O arquivo após a conversão passou de 8mb, que é o limite do Discord, tente outra imagem.**')
                deleteImagesLocal(pathToImageJPG, pathToImagePNG)

            else:

                # Send image to chat
                f = discord.File(pathToImagePNG, filename="imagePNG.png")
                embedImagem = discord.Embed(
                    title='Imagem em PNG',
                    description='_Os comandos podem ser usados juntos com o envio do arquivo._',
                    colour=discord.Colour(0x5BFD22)
                )

                embedImagem.set_image(url='attachment://imagePNG.png')
                messageWithFile = await ctx.reply(file=f, embed=embedImagem)

                # Send button with URL of image
                await ctx.send(content="_ _", components=[
                    Button(style=ButtonStyle.URL,
                           url=f"{messageWithFile.embeds[0].image.url}",
                           label='Link')
                ])

                deleteImagesLocal(pathToImageJPG, pathToImagePNG)