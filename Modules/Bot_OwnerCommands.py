#!/bin/bash/python3
#coding: utf-8

import discord


async def shutdownCommand(ctx, bot):
    
    embedShutdown = discord.Embed(
        description = '**Desligando...**',
        colour = discord.Colour(0xFF0000)
    )

    await ctx.send(embed = embedShutdown)
    await ctx.bot.logout()