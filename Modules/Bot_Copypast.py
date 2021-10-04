#!/bin/bash/python3
#coding: utf-8

import math
import json
import base64
import discord
import pandas as pd


async def copypastCommand(ctx, dictCopypasts):

    nameCopypast = ctx.invoked_with
    copypastb64 = dictCopypasts[nameCopypast]
    copypast = base64.b64decode(copypastb64.encode()).decode("utf-8")

    if len(copypast) > 2000:

        quantFor = math.ceil(len(copypast) / 1000)
        begin = 0
        ending = 1000

        for i in range(quantFor):
            await ctx.send(copypast[begin:ending])
            begin = begin + 1000
            ending = ending + 1000

    else:

        await ctx.send(copypast)

    await ctx.message.delete()


async def listCpsCommand(ctx, dictCopypasts):

    dictCopypasts = dict(sorted(dictCopypasts.items()))

    limitRangeCopypastDisplayInDiscord = 24
    beginLimitRangeCopypastDisplayInDiscord = 0
    listEmbedsCopypasts = []
    quantEmbedsCreates = math.ceil(len(dictCopypasts.keys()) / 25)

    for el in range(quantEmbedsCreates):

        listEmbedsCopypasts.append(discord.Embed(description='**Lista de copypasts**', colour=ctx.author.colour, timestamp=ctx.message.created_at))

        if el == (quantEmbedsCreates - 1):

            for cpast in list(dictCopypasts.keys())[beginLimitRangeCopypastDisplayInDiscord: len(dictCopypasts.keys())]:

                data = base64.b64decode(bytes(dictCopypasts[cpast].encode())).decode("utf-8")
                listEmbedsCopypasts[el].add_field(name='-' + cpast, value=data[0:15].lower() + '...')

        else:

            for cpast in list(dictCopypasts.keys())[beginLimitRangeCopypastDisplayInDiscord:limitRangeCopypastDisplayInDiscord]:

                data = base64.b64decode(bytes(dictCopypasts[cpast].encode())).decode("utf-8")
                listEmbedsCopypasts[el].add_field(name='-' + cpast, value=data[0:15].lower() + '...')

            beginLimitRangeCopypastDisplayInDiscord = beginLimitRangeCopypastDisplayInDiscord + 25
            limitRangeCopypastDisplayInDiscord = limitRangeCopypastDisplayInDiscord + 25

    for embedCopypast in listEmbedsCopypasts:
        await ctx.send(embed=embedCopypast)


async def addcpCommand(ctx, nameCP, textCP):

    data = base64.b64encode(bytes(textCP, 'utf-8'))
    copypastAddRow = nameCP + "," + data.decode() + "\n"

    with open('files/copypast.csv', 'a') as fd:
        fd.write(copypastAddRow)

    await ctx.send("**Adicionado.**")
