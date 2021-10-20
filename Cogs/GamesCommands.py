#!/bin/bash/python3
#coding: utf-8

import sys
import random
import aiohttp
import discord
import asyncio
from discord.ext import commands
from discord_components import Button, ButtonStyle

# Local import
sys.path.append("..")
from Utils import http

"""
Commands: duck, reverse and eightball from @AlexFlipnote

https://github.com/AlexFlipnote
https://github.com/AlexFlipnote/discord_bot.py/blob/master/cogs/fun.py
"""


class GamesCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # Command Game Rock Paper Scissors
    @commands.command(aliases=["ppt"])
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    async def rps(self, ctx):

        embedRps = discord.Embed(
            title="Rock - Paper - Scissors",
            description='Choose one',
            colour=discord.Colour(0x00FFFFFF),
            thumbnail = "https://i.imgur.com/IatSCe8.png"
        )

        embedRps.set_thumbnail(url="https://i.imgur.com/IatSCe8.png")
        embedRps.add_field(name="Time", value="`10 seconds`")

        embedRpsButton = await ctx.send(embed=embedRps, components=[
            [
                Button(label="Rock", emoji="🪨",custom_id="rock", style=ButtonStyle.red),
                Button(label="Paper", emoji="📝",custom_id="paper", style=ButtonStyle.green),
                Button(label="Scissors", emoji="✂️",custom_id="scissors", style=ButtonStyle.blue),
            ]
        ]
        )

        try:

            interaction = await self.bot.wait_for(
                "button_click", check=lambda res: res.message.id == embedRpsButton.id, timeout=10
            )

            await interaction.respond(type=6)
            await embedRpsButton.edit(embed=embedRps, components=[])

            listRps = ["rock", "paper", "scissors"]

            random.shuffle(listRps)
            listRps = random.sample(listRps, len(listRps))
            random.shuffle(listRps)

            botChoice = listRps[0]
            userChoice = interaction.custom_id

            embedRps.clear_fields()
            embedRps.title = ""
            embedRps.add_field(name=f"{interaction.user.name}", value=f"{userChoice.title()}",)
            embedRps.add_field(name=f"{self.bot.user.name}",value=f"{botChoice.title()}",)
            embedRps.set_author(name="Rock - Paper - Scissors",icon_url=interaction.user.avatar_url)

            if userChoice == botChoice:
                embedRps.add_field(name="Result", value="Tie!", inline=False)
                embedRps.colour = 0x00A4FF
                await embedRpsButton.edit(embed=embedRps, components=[])

            else:

                dictGetResult = {
                    "scissors-paper": 1,
                    "rock-scissors": 1,
                    "paper-rock": 1,
                    "paper-scissors": 0,
                    "scissors-rock": 0,
                    "rock-paper": 0
                }

                resultGame = dictGetResult[str(botChoice) + '-' + str(userChoice)]

                if resultGame == 1:
                    embedRps.add_field(name="Result", value="Lose!", inline=False)
                    embedRps.colour = 0xFF0000

                else:
                    embedRps.add_field(name="Result", value="Win!", inline=False)
                    embedRps.colour = 0x23C423

                await embedRpsButton.edit(embed=embedRps, components=[])

        except asyncio.TimeoutError:

            embedRps.clear_fields()
            embedRps.add_field(name="Time", value="`Time is over`")
            await embedRpsButton.edit(embed=embedRps, components=[])
    
    
    @commands.command(aliases=["8ball"])
    @commands.guild_only()
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        ballresponse = [
            "Yes", "No", "Take a wild guess...", "Very doubtful",
            "Sure", "Without a doubt", "Most likely", "Might be possible",
            "You'll be the judge", "no... (╯°□°）╯︵ ┻━┻", "no... baka",
            "senpai, pls no ;-;"
        ]

        answer = random.choice(ballresponse)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")
    

    @eightball.error
    async def eightballerror(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot the question.")
            ctx.handled_in_local = True


    async def randomimageapi(self, ctx, url: str, endpoint: str, token: str = None):
        try:
            r = await http.get(
                url, res_method="json", no_cache=True,
                headers={"Authorization": token} if token else None
            )
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")

        await ctx.send(r[endpoint])


    @commands.command()
    @commands.guild_only()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        """ Posts a random duck """
        await self.randomimageapi(ctx, "https://random-d.uk/api/v1/random", "url")

    
    @commands.command()
    @commands.guild_only()
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")
    
    
def setup(bot):
    bot.add_cog(GamesCommands(bot))