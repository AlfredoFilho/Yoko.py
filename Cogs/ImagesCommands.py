#!/bin/bash/python3
#coding: utf-8

import os
import random
import discord
import requests
from PIL import Image
from pathlib import Path
from discord.ext import commands
from discord_components import Button, ButtonStyle


class ImagesCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # Command convert image JPG to PNG
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(attach_files=True)
    async def tojpg(self, ctx):

        if not ctx.message.attachments:
            await ctx.send("I couldn't find a file in your message.\nUpload a **PNG** image along with the **-tojpg** command.")

        else:

            pathToImageJPG = "tmp/imageJPG-" + str(random.randint(100000, 1000000)) + ".jpg"
            pathToImagePNG = "tmp/imagePNG-" + str(random.randint(100000, 1000000)) + ".png"
            urlImageFromDiscord = ctx.message.attachments[-1].url

            if '.png' not in urlImageFromDiscord:
                await ctx.send('''
    The extension of your image is not **.png**
    Reminder: -tojpg converts PNG to JPG
    ''')
            else:
                try:
                    # os.system("wget -q -O {0} {1}".format(pathToImagePNG, urlImageFromDiscord))
                    with open(pathToImagePNG, 'wb') as f:
                        f.write(requests.get(urlImageFromDiscord).content)

                except:
                    await ctx.send('''
    **I couldn't save your image to convert :(** .
    **Possible reason:**
    - Discord Instability: Try again later.
    ''')
                    return
                try:
                    # Convert image
                    im = Image.open(pathToImagePNG)
                    rgb_im = im.convert('RGB')
                    rgb_im.save(pathToImageJPG)
                
                except:
                    
                    await ctx.send("I couldn't convert this file to JPG.\nIs this really an image? :thinking:")
                    deleteImagesLocal(pathToImageJPG, pathToImagePNG)
                    return

                # Send image to channel
                f = discord.File(pathToImageJPG, filename="imageJPG.jpg")
                embedImagem = discord.Embed(
                    title='Command -tojpg',
                    description='_Image in JPG._',
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

                self.deleteImagesLocal(pathToImageJPG, pathToImagePNG)


    def deleteImagesLocal(self, pathToImageJPG, pathToImagePNG):

        my_file = Path(pathToImageJPG)
        if my_file.is_file():
            os.remove(pathToImageJPG)
        
        my_file = Path(pathToImagePNG)
        if my_file.is_file():
            os.remove(pathToImagePNG)


    # Command convert image PNG to JPG
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(attach_files=True)
    async def topng(self, ctx):


        if not ctx.message.attachments:
            await ctx.send("I couldn't find a file in your message.\nUpload a **JPG** image along with the **-topng** command.")

        else:

            pathToImageJPG = "tmp/imageJPG-" + str(random.randint(100000, 1000000)) + ".jpg"
            pathToImagePNG = "tmp/imagePNG-" + str(random.randint(100000, 1000000)) + ".png"
            urlImageFromDiscord = ctx.message.attachments[-1].url

            if '.jpg' not in urlImageFromDiscord:
                await ctx.send('''
    The extension of your image is not **.jpg**
    Reminder: -topng converts JPG to PNG
    ''')
            else:
                try:
                    # os.system("wget -q -O {0} {1}".format(pathToImageJPG, urlImageFromDiscord))
                    with open(pathToImageJPG, 'wb') as f:
                        f.write(requests.get(urlImageFromDiscord).content)

                except:
                    await ctx.send('''
    **I couldn't save your image to convert :(** .
    **Possible reason:**
    - Discord Instability: Try again later.
    ''')
                    return
                try:
                    # Convert image
                    im = Image.open(pathToImageJPG)
                    im.save(pathToImagePNG, 'png')
                
                except:

                    await ctx.send("I couldn't convert this file to PNG.\nIs this really an image? :thinking:")
                    deleteImagesLocal(pathToImageJPG, pathToImagePNG)
                    return

                sizeImage = int(os.stat(pathToImagePNG).st_size)

                if sizeImage > 8000000:
                    await ctx.channel.send('**The file after conversion was bigger than 8mb, Discord file size limit, try another image.**')
                    deleteImagesLocal(pathToImageJPG, pathToImagePNG)

                else:

                    # Send image to chat
                    f = discord.File(pathToImagePNG, filename="imagePNG.png")
                    embedImagem = discord.Embed(
                    title='Command -topng',
                    description='_Image in PNG._',
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

                    self.deleteImagesLocal(pathToImageJPG, pathToImagePNG)


def setup(bot):
    bot.add_cog(ImagesCommands(bot))