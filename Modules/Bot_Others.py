#!/bin/bash/python3
#coding: utf-8

import json
import asyncio
import discord
import platform
from discord_components import Button, ButtonStyle, Select, SelectOption


async def pingCommand(ctx, bot):

    latencyBot = round(bot.latency * 1000)

    await ctx.send('**Opa!** _' + str(latencyBot) + 'ms_')


async def purgeCommand(ctx, quant):

    quant = quant + 1

    if quant > 100:
        quant = 100

    channelLog = ctx.message.channel
    messagesDel = await channelLog.history(limit=quant).flatten()

    await channelLog.delete_messages(messagesDel)
    await ctx.send(f"{quant-1} mensagens apagadas", delete_after=2.0)


async def statsCommand(ctx, bot):

    infoBot = await bot.application_info()

    pythonVersion = platform.python_version()
    discordPyVersion = discord.__version__

    embedStatus = discord.Embed(description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embedStatus.add_field(name='Bot Version', value='2.0')
    embedStatus.add_field(name='Python Version', value=pythonVersion)
    embedStatus.add_field(name='Discord.Py Version', value=discordPyVersion)

    embedStatus.set_footer(text=f"{bot.user.name}")
    embedStatus.set_author(name='Yoko - Stats', icon_url=bot.user.avatar_url)

    await ctx.send(embed=embedStatus)


def makeEmbedSubHelp(embedHelp, subHelpDict, subHelpFromUser):
    
    embedHelp.clear_fields()
    embedHelp.title = "Ajuda - " + subHelpFromUser.title()
    embedHelp.description = subHelpDict[subHelpFromUser]["contentEmbed"]["description"] 

    for field in subHelpDict[subHelpFromUser]["contentEmbed"]["fields"]:
        embedHelp.add_field(name=field["name"], value=field["value"], inline=field["inline"])

    return embedHelp

async def new(ctx, bot, subHelpFromUser, loadJsonFile, botId):


    subHelpDict = loadJsonFile("files/helpDescriptions.json")
    
    embedHelp = discord.Embed(
        colour=discord.Colour(0xFF0059)
    )

    embedHelp.set_thumbnail(url="https://i.imgur.com/xR7MZcj.jpg")
    embedHelp.set_footer(text="Escolha um módulo!", icon_url=ctx.message.author.avatar_url)

    if subHelpFromUser != None and subHelpFromUser.lower() in list(subHelpDict.keys()):
        
        embedHelp = makeEmbedSubHelp(embedHelp, subHelpDict, subHelpFromUser)

    else:
    
        embedHelp.title="Salve!"
        embedHelp.description=f"Servidor: `{ctx.message.guild.name}`"
        
        embedHelp.add_field(name="**<:modulesIcon:892131485132402709> Módulos:**", 
        value='''
        > ┠ Animelist
        > ┠ Copypasta
        > ┠ Imagens
        > ┠ Jogos
        > ┠ Legendas
        > ┠ Outros
        '''
        )

        embedHelp.add_field(name="**<:linkIcon:892131991636541451> Link!:**",
        value=f'''
        [Convite](https://discord.com/api/oauth2/authorize?client_id={botId}&permissions=8&scope=bot%20applications.commands)
        ''')

        embedHelp.add_field(name="<:globeIcon:892174454388588657> Mudar idioma", value="Em construção", inline=False)

    msgHelp = await ctx.send(
                embed=embedHelp,
                components=[
                    Select(
                        placeholder="Opções",
                        options=[SelectOption(
                            label = subHelp.title(),
                            description = subHelpDict[subHelp]["descriptionSelect"],
                            value = subHelp,
                            emoji=bot.get_emoji(subHelpDict[subHelp]["idEmojiSelect"])) 
                                for subHelp in subHelpDict.keys()
                        ],
                        custom_id="select1",
                    )
                ],
            )
    
    while True:
        
        try: 
            interaction = await bot.wait_for(
                "select_option", check=lambda res: res.message.id == msgHelp.id, timeout=20
            )
            
            await interaction.respond(type=6)

            subHelpFromUser = interaction.values[0]
            embedHelp = makeEmbedSubHelp(embedHelp, subHelpDict, subHelpFromUser)
            await msgHelp.edit(embed=embedHelp)
        
        except asyncio.TimeoutError:

            embedHelp.set_footer(text="Menu desativado por inatividade.", icon_url=ctx.message.author.avatar_url)
            await msgHelp.edit(embed=embedHelp, components=[])
            
            break
    