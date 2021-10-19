#!/bin/bash/python3
#coding: utf-8

import random
import discord
import asyncio
from discord.ext import commands
from discord_components import Button, ButtonStyle


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
    
    
def setup(bot):
    bot.add_cog(GamesCommands(bot))