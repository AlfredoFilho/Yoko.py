# coding: utf-8

import sys
import discord
import YokoFuncs
from discord import User
from threading import Timer
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import *


#Definir prefixo
client = commands.Bot(command_prefix = '-')


@client.event
async def on_ready():
    
    print('---------------------')
    print('       ONLINE        ')
    print('---------------------\n')
    
    await client.change_presence(status = discord.Status.online, activity = discord.Game('-ajuda'))


@client.event
async def on_message(message):

    global msg
    global url_ultimo_arq

    msg = message

    try:
        url_ultimo_arq = message.attachments[-1].url
        t = Timer(5.0, limparUltimoArq)
        t.start()

    except:
        pass
    
    await client.process_commands(message)


def limparUltimoArq():

    global url_ultimo_arq
    url_ultimo_arq = None


#==========================================================
#Comandos
def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)


@client.command(aliases=['purge'])
@commands.check_any(is_guild_owner())
async def _purge(ctx, *quant):

    if int(quant[0]) > 0:

        quantidade = int(quant[0]) + 1 

        if quantidade > 99:
            quantidade = 99

        channelLog = ctx.message.channel
        messagesDel = await channelLog.history(limit = int(quantidade)).flatten()
        await channelLog.delete_messages(messagesDel)
        

    else:
        await ctx.send("Valor especificado deve ser número e maior que 0. Exemplo de como usar: `-purge 10`")


@client.command()
@commands.is_owner()
async def shutdown(ctx):
    #Desligar Bot
    
    await YokoFuncs.shutdownCommand(ctx, client)


@client.command()
async def stats(ctx):
    #Algumas estatíscicas do Bot

    await YokoFuncs.statsCommand(ctx, client)


@client.command(aliases=['ajuda'])
async def _ajuda(ctx, *subajuda):
    #Comando de ajuda

    await YokoFuncs.ajudaCommand(ctx, client, subajuda)


@client.command()
async def ping(ctx):
    #Ping do Bot

    await YokoFuncs.pingCommand(ctx, client)


@client.command(aliases=['trad'])
async def _trad(ctx, lang, *, texto):
    #Traduz texto inserido para lingua informada
    
    await YokoFuncs.tradCommand(ctx, client, lang, texto)


@client.command()
async def topng(ctx):
    #Converte imagem JPG para PNG

    global url_ultimo_arq

    await YokoFuncs.topngCommand(ctx, client, url_ultimo_arq)


@client.command()
async def tojpg(ctx):
    #Converte imagem PNG para JPG  

    global url_ultimo_arq

    await YokoFuncs.tojpgCommand(ctx, client, url_ultimo_arq)
    

@client.command(aliases=['anilist'])
async def _anilist(ctx, usernameAnilist, *, tipo):
    #Escolhe um randomico do perfil no Anilist do PTW

    global url_ultimo_arq

    await YokoFuncs.anilistCommand(ctx, client, url_ultimo_arq, usernameAnilist, tipo)
    

#==========================================================
#Comandos de ERROS
@_purge.error
async def purge_error(ctx, error):
    
    embedPermissao = discord.Embed(
        title = "Fail - Possíveis Motivos",
        description = '- Não tenho permissão para Gerenciar Mensagens.\n- Só posso deletar mensagens de até 14 dias atrás.\n- Somente o **dono** do servidor pode usar esse comando.',
        colour = discord.Colour(0xFF0000)
    )
    
    await ctx.send(embed = embedPermissao)


@shutdown.error
async def shutdown_error(ctx, error):
    
    embedPermissao = discord.Embed(
        description = '**Aí não né! Você não tem permissão para esse comando.**',
        colour = discord.Colour(0xFF0000)
    )
    
    await ctx.send(embed = embedPermissao)
    

@_trad.error
async def trad_error(ctx, error):

    embedTrans = discord.Embed(
        title = "Calmoo :raised_hand:",
        description = 'Essa língua não existe, consulte as línguas aqui: [Línguas](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages) 🔗',
        colour = discord.Colour(0xFF0000)
    )
    
    await ctx.send(embed = embedTrans)
    print('Fim-ErroTrad\n')


@topng.error
async def topng_error(ctx, error): 

    await YokoFuncs.erroCommand(ctx, error)
    print('Fim-ErroTopng\n')
     

@tojpg.error
async def tojpg_error(ctx, error): 

    await YokoFuncs.erroCommand(ctx, error)
    print('Fim-ErroTojpg\n')


@_anilist.error
async def anilist_error(ctx, error):

    desc = '''
Possíveis motivos:
- Usuário não existe
- Anilist fora do ar
'''

    if isinstance(error, BadArgument):
        desc = '''
Esse **tipo** não existe, use **anime** ou **manga**
_Se tiver algum espaço após o **tipo**, retire-o._       
'''

    embedErro = discord.Embed(
                title = ':raised_hand: Erro :raised_back_of_hand:',
                description = desc,
                colour = discord.Colour(0xF2070B)
            )

    await ctx.channel.send(embed=embedErro)

    print('Fim-AnilistError\n')

#=================================================

#Algumas variaveis globais
msg = None
url_ultimo_arq = None

#Remover comando padrão help
client.remove_command('help')

#Iniciar Bot
TOKEN = 'yourTokenBot'
client.run(TOKEN)