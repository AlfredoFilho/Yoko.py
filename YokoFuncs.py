import os
import re
import json
import codecs
import random
import discord
import requests
from PIL import Image
import urllib.request
from datetime import datetime
from discord.ext.commands import *
from discord.ext.commands import BadArgument


async def pingCommand(ctx, client):
    
    latencia = round(client.latency * 1000)
    await ctx.send('**Opa!** _' + str(latencia) + 'ms_')


async def shutdownCommand(ctx, client):
    
    embedDesligar = discord.Embed(
        description = '**Desligando...**',
        colour = discord.Colour(0xFF0000)
    )

    await ctx.send(embed = embedDesligar)
    await ctx.bot.logout()


async def tradCommand(ctx, client, lang, texto):

    import googletrans

    translator = googletrans.Translator()
    traducao = translator.translate(texto, lang)    
    textoTrad = traducao.text
    await ctx.send('----------------------------------------------------------\n**Original:** '+texto+'\n**Tradução:** '+textoTrad + '\n----------------------------------------------------------')


async def statsCommand(ctx, client):

    import platform

    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members()))

    embedStatus = discord.Embed(title = f'{client.user.name} Stats', description = '\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embedStatus.add_field(name = 'Bot Version', value = '2.0')
    embedStatus.add_field(name = 'Python Version', value = pythonVersion)
    embedStatus.add_field(name = 'Discord.Py Version', value = dpyVersion)
    # embedStatus.add_field(name = 'Total Servers:', value = serverCount)
    # embedStatus.add_field(name = 'Total Users:', value = memberCount)
    # embedStatus.add_field(name = 'Bot Developers:', value = '<@528210231272931338>')

    embedStatus.set_footer(text = f"{client.user.name}")
    embedStatus.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    await ctx.send(embed=embedStatus)


async def ajudaCommand(ctx, client, subajuda):
    
    listaAjudas = ['imagens', 'animelist', 'texto']

    if ((len(subajuda) == 1) and (subajuda[0] in listaAjudas)):
        
        if(subajuda[0] == 'imagens'):

            embedAjuda = discord.Embed(
                title = 'Imagens',
                description = '''

**-topng** -> Converte imagem JPG para PNG
**-tojpg** -> Converte imagem PNG para JPG

`Pode-se enviar a imagem juntamente com o comando, ou só a imagem e usar o comando depois (5sg).`
''',
                colour = discord.Colour(0xFF0059)
            )

            await ctx.send(embed=embedAjuda)

        if(subajuda[0] == 'animelist'):

            embedAjuda = discord.Embed(
                title = 'AnimeList',
                description = '''
Escolhe um randômico da lista de PTW ou PTR

**tipo** = manga ou anime
**nome** = nome de usuário no Anilist (se usar o -anilist)

-anilist nome tipo

**Exemplo:** `-anilist Zezin anime`
Vai escolher um randômico da lista de PTW do Zezin no Anilist
''',
                colour = discord.Colour(0xFF0059)
            )

            await ctx.send(embed=embedAjuda)

        if(subajuda[0] == 'texto'):

            embedAjuda = discord.Embed(
                title = 'Texto',
                description = '''
-translate língua texto -> traduzirá o texto para a língua que for informada

**Exemplo:** `-translate pt Good morning`
[Línguas](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages) 🔗
''',
                colour = discord.Colour(0xFF0059)
            )

            await ctx.send(embed=embedAjuda)

    else:

        embedAjuda = discord.Embed(
            title = 'Convite',
            url = "https://discordapp.com/oauth2/authorize?client_id=613476064299188224&scope=bot&permissions=125952",
            colour = discord.Colour(0xFF0059)
        )

        embedAjuda.set_thumbnail(url = "https://i.imgur.com/xR7MZcj.jpg")
        embedAjuda.add_field(name = "**Imagens**", value = "`-ajuda imagens`", inline = "False")
        embedAjuda.add_field(name = "**AnimeList**", value = "`-ajuda animelist`", inline = "False")
        embedAjuda.add_field(name = "**Texto**", value = "`-ajuda texto`", inline = "False")
        embedAjuda.add_field(name = "**Stats**", value = "`-stats`", inline = "True")
        embedAjuda.add_field(name = "**Ping**", value = "`-ping`", inline = "True")
        embedAjuda.add_field(name = "**Apagar mensagens**", value = "`ex: -purge 10`", inline = "True")

        await ctx.send(embed=embedAjuda)


async def topngCommand(ctx, client, url_ultimo_arq):

    if url_ultimo_arq == None:
        await ctx.send('Envie uma imagem **JPG** e em seguida utilize o comando **-topng**')
    else:
        if '.jpg' not in url_ultimo_arq:
            await ctx.send('''
A extensão da sua imagem não é **.jpg**
Lembrete: -topng converte JPG para PNG
''')
        else:
            try:
                out_image = 'imagemJPG.jpg'
                os.system("wget -q -O {0} {1}".format(out_image, url_ultimo_arq))

                im = Image.open('imagemJPG.jpg')
                im.save('imagemPNG.png','png')

                sizeImagem = int(os.stat('imagemPNG.png').st_size)

                if sizeImagem > 8000000:
                    await ctx.channel.send('O arquivo final passou de 8mb que é limite do Discord, tente outra imagem.')

                else:
                    
                    #Enviar imagem para o chat
                    f = discord.File("imagemPNG.png", filename="imagemPNG.png")
                    embedImagem = discord.Embed(
                            title = 'Imagem em PNG',
                            description = '_Os comandos podem ser usados juntos com o envio do arquivo._',
                            colour = discord.Colour(0x5BFD22)
                        )

                    embedImagem.set_image(url='attachment://imagemPNG.png')
                    await ctx.channel.send(file=f, embed=embedImagem)
            
                    #Remover imagem
                    os.remove('imagemJPG.jpg')
                    os.remove('imagemPNG.png')
            
            except:
                await ctx.send('''
Não consegui salvar sua imagem para converter :( .
**Possível motivo:**
- Instabilidade no Discord: Tente novamente mais tarde.
Lembrete: -topng converte JPG para PNG
''')

async def tojpgCommand(ctx, client, url_ultimo_arq):

    if url_ultimo_arq == None:
        await ctx.send('Envie uma imagem **PNG** e em seguida utilize o comando **-tojpg**')
    else:
        if '.png' not in url_ultimo_arq:
            await ctx.send('''
A extensão da sua imagem não é **.png**
Lembrete: -tojpg converte PNG para JPG
''')
        else:
            try:
                out_image = 'imagemPNG.png'
                os.system("wget -q -O {0} {1}".format(out_image, url_ultimo_arq))

                im = Image.open("imagemPNG.png")
                rgb_im = im.convert('RGB')
                rgb_im.save('imagemJPG.jpg')

                #Enviar imagem para o chat
                f = discord.File("imagemJPG.jpg", filename="imagemJPG.jpg")
                embedImagem = discord.Embed(
                        title = 'Imagem em JPG',
                        description = '_Os comandos podem ser usados juntos com o envio do arquivo._',
                        colour = discord.Colour(0xFF007F)
                    )

                embedImagem.set_image(url='attachment://imagemJPG.jpg')
                await ctx.channel.send(file=f, embed=embedImagem)
        
                #Remover imagem
                os.remove('imagemJPG.jpg')
                os.remove('imagemPNG.png')
            
            except:
                await ctx.send('''
Não consegui salvar sua imagem para converter :( .
**Possível motivo:**
- Instabilidade no Discord: Tente novamente mais tarde.
Lembrete: -tojpg converte PNG para JPG
''')

async def anilistCommand(ctx, client, url_ultimo_arq, usernameAnilist, tipo):

    url = 'https://graphql.anilist.co'

    variables = {
        'username': '',
        'type': '',
        'status' : 'PLANNING'
    }

    queryManga = '''
    query ($username: String, $type: MediaType, $status: MediaListStatus) {
        MediaListCollection(userName: $username, type: $type, status : $status) {
            user{
                avatar {
                    large
                }
            }
            lists {
                entries {
                    status
                    media {
                        siteUrl
                        status
                        volumes
                        chapters
                        meanScore
                        genres
                        startDate {
                            year
                        }
                        title {
                            romaji
                        }
                        coverImage {
                            extraLarge
                        }
                    }
                }
            }
        }
    }
    '''

    queryAnime = '''
    query ($username: String, $type: MediaType, $status: MediaListStatus) {
        MediaListCollection(userName: $username, type: $type, status : $status) {
            user{
                avatar {
                    large
                }
            }
            lists {
                entries {
                    status
                    media {
                        siteUrl
                        episodes
                        genres
                        meanScore
                        seasonYear
                        title {
                            romaji
                        }
                        coverImage {
                            extraLarge
                        }
                    }
                }
            }
        }
    }
    '''

    usuario = usernameAnilist
    tipo = tipo

    if (tipo.upper() == 'MANGA'):
        query = queryManga
        colorHex = 0x23C423

    elif (tipo.upper() == 'ANIME'):
        query = queryAnime
        colorHex = 0x00A4FF

    else:
        raise BadArgument

    variables['username'] = usuario
    variables['type'] = tipo.upper()

    #resultado url
    response = requests.post(url, json={'query': query, 'variables': variables})
    
    #resultado para json
    jsonV = json.loads(response.text)
    
    #lista de respostas
    listaRespostas = jsonV['data']['MediaListCollection']['lists'][0]['entries']
    
    #embaralhar lista
    random.shuffle(listaRespostas)
    listaRespostas = random.sample(listaRespostas, len(listaRespostas))
    random.shuffle(listaRespostas)

    urlMediaAnilist = str(listaRespostas[0]['media']['siteUrl'])
    urlMediaImg = str(listaRespostas[0]['media']['coverImage']['extraLarge'])
    urlImagemUser = str(jsonV['data']['MediaListCollection']['user']['avatar']['large'])

    #criar embed
    embedRandomAnilist = discord.Embed(
        title = str(listaRespostas[0]['media']['title']['romaji']),
        url = urlMediaAnilist,
        colour = discord.Colour(colorHex)
    )

    embedRandomAnilist.set_image(url = urlMediaImg)

    if (tipo.upper() == 'ANIME'):
        embedRandomAnilist.add_field(name = "Episódios", value = str(listaRespostas[0]['media']['episodes']))
        embedRandomAnilist.add_field(name = "Ano", value = str(listaRespostas[0]['media']['seasonYear']))
        embedRandomAnilist.add_field(name = "Nota", value = str(int(listaRespostas[0]['media']['meanScore']) / 10))

    else:
        embedRandomAnilist.add_field(name = "Capítulos", value = str(listaRespostas[0]['media']['chapters']))
        embedRandomAnilist.add_field(name = "Ano", value = str(listaRespostas[0]['media']['startDate']['year']))
        embedRandomAnilist.add_field(name = "Nota", value = str(int(listaRespostas[0]['media']['meanScore']) / 10))

    generosAnime = listaRespostas[0]['media']['genres']
    generosAnimeStr = ', '.join(generosAnime)

    embedRandomAnilist.add_field(name = "Gêneros", value = generosAnimeStr, inline = False)
    embedRandomAnilist.set_footer(text = 'Anilist - '+ str(usuario), icon_url = urlImagemUser)

    await ctx.channel.send(embed=embedRandomAnilist)


async def erroCommand(ctx, error):

    if isinstance(error, MissingPermissions):
       await ctx.send("Não tenho permissão para usar esse comando!")
    
    else:

        embedErro = discord.Embed(
            title = 'Erro',
            description = '''
    Calmoo :raised_hand:
    Tu fez algo errado! Use: **-ajuda**
    ''',
            colour = discord.Colour(0xF2070B)
        )

        await ctx.channel.send(embed=embedErro)
