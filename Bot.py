#!/bin/bash/python3
#coding: utf-8
import discord
import pandas as pd
from pathlib import Path
from discord.ext import commands, tasks
from discord_components import DiscordComponents

from Modules import Bot_Games
from Modules import Bot_Images
from Modules import Bot_Others
from Modules import Bot_Errors
from Modules import Bot_Copypast
from Modules import Bot_Subtitles
from Modules import Bot_AnimeList
from Modules import Bot_OwnerCommands
from Modules.getFiles import getJsonData, getDictFromCsv


bot = commands.Bot(command_prefix=';', help_command=None)
DiscordComponents(bot)

dataConfiguration = getJsonData("configuration.json")
TOKEN = dataConfiguration["token"]

# Create tmp folder if not exists
Path("tmp").mkdir(parents=True, exist_ok=True)


@bot.event
async def on_ready():

    # iniciarBanco()

    print('---------------------')
    print('       ONLINE        ')
    print('---------------------\n')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(';ajuda'))


# Command help
@bot.command(aliases=['ajuda'])
async def help(ctx, subHelp : str=None):

    await Bot_Others.new(ctx, bot, subHelp, getJsonData, bot.user.id)


# Command convert image JPG to PNG
@bot.command()
@commands.bot_has_permissions(attach_files=True)
async def topng(ctx):

    await Bot_Images.topngCommand(ctx)
    

# Command convert image PNG to JPG
@bot.command()
@commands.bot_has_permissions(attach_files=True)
async def tojpg(ctx):

    await Bot_Images.tojpgCommand(ctx)


# Command purge - delete messages
@bot.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def _purge(ctx, quant: int):

    await Bot_Others.purgeCommand(ctx, quant)


@_purge.error
async def purge_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltou a quantidade.")
        ctx.handled_in_local = True


# Command Game Rock Paper Scissors
@bot.command(aliases=["ppt"])
@commands.bot_has_permissions(manage_messages=True)
async def rps(ctx):

    await Bot_Games.rpsCommand(ctx, bot)


# Command copypast - send a copypast from files/copypast.csv
dictCopypasts = getDictFromCsv('files/copypast.csv')
aliasesCopypasts = list(dictCopypasts.keys())

@bot.command(aliases=aliasesCopypasts)
@commands.bot_has_permissions(manage_messages=True)
async def _copypast(ctx):

    global dictCopypasts
    await Bot_Copypast.copypastCommand(ctx, dictCopypasts)


# Command listacp - list of copypasts availabre from files/copypast.csv
@bot.command(aliases=['listacp'])
async def listarcp(ctx):

    await Bot_Copypast.listCpsCommand(ctx, dictCopypasts)


# Function to update aliases of command "_copypast" after add new copypast with addcp command
def update_aliases(command, *aliases):
    
    bot.remove_command(command.name)
    command.aliases.extend(aliases)
    bot.add_command(command)


# Command to add new copypast
@bot.command()
async def addcp(ctx, nameCP, *, textCP):

    if len(textCP) < 10:
        await ctx.send("Tamanho da copypast deve ser de pelo menos 10 caracteres.")
    
    else:

        reservedWordsFromOtherCommands = list(bot.all_commands.keys())

        global aliasesCopypasts
        global dictCopypasts

        if nameCP not in aliasesCopypasts and nameCP not in reservedWordsFromOtherCommands:

            await Bot_Copypast.addcpCommand(ctx, nameCP, textCP)

            # update aliases after add new copypast
            dictCopypasts = getDictFromCsv('files/copypast.csv')
            aliasesCopypasts = list(dictCopypasts.keys())
            update_aliases(_copypast, nameCP)

        else:
            await ctx.send("Essa copypast **já existe** ou usou um **nome reservado de outro comando**.")


@addcp.error
async def addcp_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltou um argumento.\nExemplo: -addcp __teste__ __isso é teste de exemplo__.")
        ctx.handled_in_local = True


# Command stats - infos bot
@bot.command()
async def stats(ctx):

    await Bot_Others.statsCommand(ctx, bot)


# Command ping - latency the bot
@bot.command()
async def ping(ctx):

    await Bot_Others.pingCommand(ctx, bot)


# Command to shutdown the bot
@bot.command()
@commands.is_owner()
async def shutdown(ctx):

    await Bot_OwnerCommands.shutdownCommand(ctx, bot)


# Errors
@bot.event
async def on_command_error(ctx, error):

    if hasattr(ctx, "handled_in_local"):
        if ctx.handled_in_local == True:
            return

    if isinstance(error, (commands.MissingPermissions, commands.BotMissingPermissions)):
        await ctx.send(error)
    

# Run
bot.run(TOKEN)