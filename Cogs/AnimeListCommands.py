#!/bin/bash/python3
#coding: utf-8

import json
import random
import discord
import requests
from discord.ext import commands


class AnimeListCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    
    # Function to check response of field from Anilist is empty
    def getValue(self, position):

        if position == None:
            return "X"

        else:
            return position


    # Command to choose a random from the user list in Anilist
    @commands.command()
    @commands.guild_only()
    async def anilist(self, ctx, usernameAnilist: str, fromList: str):

        fromList = fromList.upper()

        if fromList != "ANIME" and fromList != "MANGA":
            raise commands.BadArgument
        
        else:

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
                await ctx.send("User not found.")

            else:

                if not jsonResponses['data']['MediaListCollection']['lists']:
                    await ctx.send(f"This user does not have any {fromList.lower()} in planning.")

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

                    if (fromList == 'ANIME'):
                        embedRandomAnilist.add_field(name="Episodes", value=self.getValue(listWithResponses[0]['media']['episodes']))
                        embedRandomAnilist.add_field(name="Year", value=self.getValue(listWithResponses[0]['media']['seasonYear']))
                        embedRandomAnilist.add_field(name="Score", value=str(score))

                    else:
                        embedRandomAnilist.add_field(name="Chapters", value=self.getValue(listWithResponses[0]['media']['chapters']))
                        embedRandomAnilist.add_field(name="Year", value=self.getValue(listWithResponses[0]['media']['startDate']['year']))
                        embedRandomAnilist.add_field(name="Score", value=str(score))

                    genresList = self.getValue(listWithResponses[0]['media']['genres'])

                    try:
                        genresString = ', '.join(genresList)

                    except:
                        genresString = "X"

                    embedRandomAnilist.add_field(name="Genres", value=genresString, inline=False)
                    embedRandomAnilist.set_footer(text='Anilist - ' + str(usernameAnilist), icon_url=urlImageUser)

                    await ctx.channel.send(embed=embedRandomAnilist)
    

    # Handle error Missing Argument and Bad Argument for command anilist
    @anilist.error
    async def anilist_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot some parameter. Example: `-anilist Bayon anime`")
            ctx.handled_in_local = True


        if isinstance(error, commands.BadArgument):
            await ctx.send("This option does not exist. Options: `anime` and `manga`.\nExample: `-anilist Bayon anime`")
            ctx.handled_in_local = True


def setup(bot):
    bot.add_cog(AnimeListCommands(bot))