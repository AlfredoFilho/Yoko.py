#!/bin/bash/python3
#coding: utf-8

import random
import discord
import asyncio
from discord_components import Button, ButtonStyle


async def rpsCommand(ctx, bot):

    embedRps = discord.Embed(
        title="Pedra - Papel - Tesoura",
        description='Escolha um para duelar contra o bot.',
        colour=discord.Colour(0x00FFFFFF),
        thumbnail = "https://i.imgur.com/fhehwHx.png"
    )

    embedRps.set_thumbnail(url="https://i.imgur.com/fhehwHx.png")
    embedRps.add_field(name="Tempo", value="`10 segundos`")

    embedRpsButton = await ctx.send(embed=embedRps, components=[
        [
            Button(label="Pedra", emoji="🪨",custom_id="pedra", style=ButtonStyle.red),
            Button(label="Papel", emoji="📝",custom_id="papel", style=ButtonStyle.green),
            Button(label="Tesoura", emoji="✂️",custom_id="tesoura", style=ButtonStyle.blue),
        ]
    ]
    )

    try:

        interaction = await bot.wait_for(
            "button_click", check=lambda res: res.message.id == embedRpsButton.id, timeout=10
        )

        await interaction.respond(type=6)
        await embedRpsButton.edit(embed=embedRps, components=[])

        listRps = ["pedra", "papel", "tesoura"]

        random.shuffle(listRps)
        listRps = random.sample(listRps, len(listRps))
        random.shuffle(listRps)

        botChoice = listRps[0]
        userChoice = interaction.custom_id

        embedRps.clear_fields()
        embedRps.title = ""
        embedRps.add_field(name=f"{interaction.user.name}", value=f"{userChoice.title()}",)
        embedRps.add_field(name=f"{bot.user.name}",value=f"{botChoice.title()}",)
        embedRps.set_author(name="Pedra - Papel - Tesoura",icon_url=interaction.user.avatar_url)

        if userChoice == botChoice:
            embedRps.add_field(name="Resultado", value="Empate!", inline=False)
            embedRps.colour = 0x00A4FF
            await embedRpsButton.edit(embed=embedRps, components=[])

        else:

            dictGetResult = {
                "tesoura-papel": 1,
                "pedra-tesoura": 1,
                "papel-pedra": 1,
                "papel-tesoura": 0,
                "tesoura-pedra": 0,
                "pedra-papel": 0
            }

            resultGame = dictGetResult[str(botChoice) + '-' + str(userChoice)]

            if resultGame == 1:
                embedRps.add_field(name="Resultado", value="Perdeu!", inline=False)
                embedRps.colour = 0xFF0000

            else:
                embedRps.add_field(name="Resultado", value="Ganhou!", inline=False)
                embedRps.colour = 0x23C423

            await embedRpsButton.edit(embed=embedRps, components=[])

    except asyncio.TimeoutError:

        embedRps.clear_fields()
        embedRps.add_field(name="Tempo", value="`Esgotado`")
        await embedRpsButton.edit(embed=embedRps, components=[])
