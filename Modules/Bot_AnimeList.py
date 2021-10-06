#!/bin/bash/python3
#coding: utf-8


import json
import random
import discord
import requests


def getValue(position):

    if position == None:
        return "X"

    else:
        return position


async def anilistCommand(ctx, usernameAnilist, fromList):

    urlApiAnilist = 'https://graphql.anilist.co'

    variables = {
        'username': '',
        'type': '',
        'status': 'PLANNING'
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

    # Manga
    if (fromList == 'MANGA'):
        query = queryManga
        colorHex = 0x23C423

    # Anime
    else:
        query = queryAnime
        colorHex = 0x00A4FF

    variables['username'] = usernameAnilist
    variables['type'] = fromList

    # resultado url
    response = requests.post(urlApiAnilist, json={'query': query, 'variables': variables})

    # Response to json
    jsonResponses = json.loads(response.text)

    if "errors" in jsonResponses.keys():
        await ctx.send("Usuário não encontrado.")

    else:

        if not jsonResponses['data']['MediaListCollection']['lists']:
            await ctx.send(f"Esse usuário não possui nenhum {fromList.lower()} no planning.")

        else:

            # List with responses
            listWithResponses = jsonResponses['data']['MediaListCollection']['lists'][0]['entries']

            # Shuffle list with responses
            random.shuffle(listWithResponses)
            listWithResponses = random.sample(listWithResponses, len(listWithResponses))
            random.shuffle(listWithResponses)

            urlMediaInAnilist = str(listWithResponses[0]['media']['siteUrl'])
            urlImageMedia = str(listWithResponses[0]['media']['coverImage']['extraLarge'])
            urlImageUser = str(jsonResponses['data']['MediaListCollection']['user']['avatar']['large'])

            # Create embed
            embedRandomAnilist = discord.Embed(
                title=str(listWithResponses[0]['media']['title']['romaji']),
                url=urlMediaInAnilist,
                colour=discord.Colour(colorHex)
            )

            embedRandomAnilist.set_image(url=urlImageMedia)

            if listWithResponses[0]['media']['meanScore'] == None:
                score = "X"

            else:
                score = listWithResponses[0]['media']['meanScore'] / 10

            if (fromList.upper() == 'ANIME'):
                embedRandomAnilist.add_field(name="Episódios", value=getValue(listWithResponses[0]['media']['episodes']))
                embedRandomAnilist.add_field(name="Ano", value=getValue(listWithResponses[0]['media']['seasonYear']))
                embedRandomAnilist.add_field(name="Nota", value=str(score))

            else:
                embedRandomAnilist.add_field(name="Capítulos", value=getValue(listWithResponses[0]['media']['chapters']))
                embedRandomAnilist.add_field(name="Ano", value=getValue(listWithResponses[0]['media']['startDate']['year']))
                embedRandomAnilist.add_field(name="Nota", value=str(score))

            genresList = getValue(listWithResponses[0]['media']['genres'])

            try:
                genresString = ', '.join(genresList)

            except:
                genresString = "X"

            embedRandomAnilist.add_field(name="Gêneros", value=genresString, inline=False)
            embedRandomAnilist.set_footer(text='Anilist - ' + str(usernameAnilist), icon_url=urlImageUser)

            await ctx.channel.send(embed=embedRandomAnilist)
