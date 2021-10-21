#!/bin/bash/python3
#coding: utf-8

import sys
import asyncio
import discord
from discord.ext import commands
from discord_components import *

# Local import
sys.path.append("..")
from Utils.getfiles import getJsonData


class HelpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    def makeEmbedSubHelp(self, embedHelp, subHelpDict, subHelpFromUser):
        
        embedHelp.clear_fields()
        embedHelp.title = "Help - " + subHelpFromUser.title()
        embedHelp.description = subHelpDict[subHelpFromUser]["contentEmbed"]["description"] 

        for field in subHelpDict[subHelpFromUser]["contentEmbed"]["fields"]:

            embedHelp.add_field(name=field["name"], value=field["value"], inline=field["inline"])

        return embedHelp


    # Command help
    @commands.command(aliases=['ajuda'])
    @commands.guild_only()
    async def help(self, ctx, subHelpFromUser : str=None):

        subHelpDict = getJsonData(self.bot.pathToJSONHelpDescriptions)
        
        embedHelp = discord.Embed(
            colour=discord.Colour(0xFF0059)
        )

        embedHelp.set_thumbnail(url="https://i.imgur.com/xR7MZcj.jpg")
        embedHelp.set_footer(text="Choose a module!", icon_url=ctx.message.author.avatar_url)

        if subHelpFromUser != None and subHelpFromUser.lower() in list(subHelpDict.keys()):
            
            embedHelp = self.makeEmbedSubHelp(embedHelp, subHelpDict, subHelpFromUser)

        else:
        
            embedHelp.title="Hey!"
            embedHelp.description=f"Server: `{ctx.message.guild.name}`"
            
            embedHelp.add_field(name="**<:modulesIcon:892131485132402709> Modules:**", 
            value='''
            > ┠ Animelist
            > ┠ Copypasta
            > ┠ Images
            > ┠ Games
            > ┠ Subtitles
            > ┠ Others
            '''
            )

            embedHelp.add_field(name="**<:linkIcon:892131991636541451> Link!:**",
            value=f'''
            [Invite]({discord.utils.oauth_url(client_id=self.bot.user.id, permissions=discord.Permissions.all())})
            ''')

            embedHelp.add_field(name="<:globeIcon:892174454388588657> Change language", value="In development", inline=False)

        msgHelp = await ctx.send(
                    embed=embedHelp,
                    components=[
                        Select(
                            placeholder="Options",
                            options=[SelectOption(
                                label = subHelp.title(),
                                description = subHelpDict[subHelp]["descriptionSelect"],
                                value = subHelp,
                                emoji=self.bot.get_emoji(subHelpDict[subHelp]["idEmojiSelect"])) 
                                    for subHelp in subHelpDict.keys()
                            ],
                            custom_id="select1",
                        )
                    ],
                )
        
        while True:
            
            try: 
                interaction = await self.bot.wait_for(
                    "select_option", check=lambda res: res.message.id == msgHelp.id, timeout=30
                )
                
                await interaction.respond(type=6)

                subHelpFromUser = interaction.values[0]
                embedHelp = self.makeEmbedSubHelp(embedHelp, subHelpDict, subHelpFromUser)
                await msgHelp.edit(embed=embedHelp)
            
            except asyncio.TimeoutError:

                embedHelp.set_footer(text="Menu disabled by inactivity.", icon_url=ctx.message.author.avatar_url)
                await msgHelp.edit(embed=embedHelp, components=[])
                
                break


def setup(bot):
    bot.add_cog(HelpCommand(bot))