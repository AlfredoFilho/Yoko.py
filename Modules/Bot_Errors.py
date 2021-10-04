#!/bin/bash/python3
#coding: utf-8

import discord


async def badArgument(ctx):

    embedBadArgument = discord.Embed(
        description='Você usou um parãmetro errado nesse comando.\nUse **-ajuda** para mais informações e exemplos.',
        colour=discord.Colour(0xFF0000)
    )

    await ctx.send(embed=embedBadArgument)


async def botMissingPermissions(ctx):

    embedBotMissingPermissions = discord.Embed(
        description='<:error:891849994196361247>  Me falta permissões para esse comando.',
        colour=discord.Colour(0xFF0000)
    )

    await ctx.send(embed=embedBotMissingPermissions)


async def userMissingPermissions(ctx):

    embedUserMissingPermissions = discord.Embed(
        description='<:error:891849994196361247>  Você não tem permissão para esse comando.',
        colour=discord.Colour(0xFF0000)
    )

    await ctx.send(embed=embedUserMissingPermissions)
