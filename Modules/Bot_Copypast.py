#!/bin/bash/python3
#coding: utf-8

import os
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

        quantFor = math.ceil(len(copypast) / 1990)

        begin = 0
        ending = 1990

        for i in range(quantFor):
            await ctx.send(copypast[begin:ending])
            begin = begin + 1990
            ending = ending + 1990

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

        listEmbedsCopypasts.append(discord.Embed(
            description='**Lista de copypasts**', colour=ctx.author.colour, timestamp=ctx.message.created_at))

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


async def addcpCommand(ctx, nameCP, textCP, pathToCSV):

    data = base64.b64encode(bytes(textCP, 'utf-8'))
    # copypastAddRow = nameCP + "," + data.decode() + "\n"
    copypastAddRow = nameCP + "," + data.decode() + "," + \
        str(ctx.message.author.id) + "\n"

    with open(pathToCSV, 'a') as fd:
        fd.write(copypastAddRow)

    await ctx.send("**Adicionado.**")


async def deletecpCommand(ctx, nameCP, update_aliases, _copypast, pathToCSV):

    df = pd.read_csv(pathToCSV)

    if nameCP not in df.nameCP.values:
        await ctx.send("Essa copypast não existe.")

    else:
        for x in range(len(df.nameCP)):
            if nameCP == df.nameCP[x]:
                if ctx.message.author.id != int(df.userWhoAdded[x]):
                    await ctx.send("Você só pode remover as que adicionou.")

                else:
                    newDF = df.drop(df.index[x])

                    # Remove old csv
                    os.remove(pathToCSV)

                    # Save new csv
                    newDF.to_csv(pathToCSV, encoding='utf-8', index=False)

                    await ctx.send(f"A copypast `{nameCP}` foi deletada.")

                    update_aliases(_copypast, nameCP, action="remove")