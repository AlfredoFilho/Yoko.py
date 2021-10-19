#!/bin/bash/python3
#coding: utf-8

import os
import sys
import math
import json
import base64
import discord
import pandas as pd
from discord.ext import commands

# Local import
sys.path.append("..")
from Modules.GetFiles import getDictFromCsv


# Get names copypastas to initialize command _copypasta
def initCommandCopypast():

    dictCopypasts = getDictFromCsv(pathToCsv='files/DataCopypast.csv', nameKey="nameCP", nameValue="textCP")
    aliasesCopypasts = list(dictCopypasts.keys())

    return aliasesCopypasts
    

class CopypastaCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.updateVarAliasesCopypasts()


    def updateVarAliasesCopypasts(self):

        self.bot.dictCopypasts = getDictFromCsv(pathToCsv='files/DataCopypast.csv', nameKey="nameCP", nameValue="textCP")
        self.bot.aliasesCopypasts = list(self.bot.dictCopypasts.keys())


    # Function to update aliases of command "_copypast" after add new copypasta or delete copypast
    def update_aliases(self, command, aliases, action):

        self.bot.remove_command(command.name)

        if action == "update":
            command.aliases.extend(aliases)
        
        else:
            command.aliases.remove(aliases)

        self.bot.add_command(command)
        self.updateVarAliasesCopypasts()

    
    # Command copypasta - send a copypasta from files/DataCopypast.csv
    @commands.command(aliases=initCommandCopypast())
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    async def _copypasta(self, ctx):

        nameCopypast = ctx.invoked_with
        copypastb64 = self.bot.dictCopypasts[nameCopypast]
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


    # Command listacp - list of copypasts available from files/DataCopypast.csv
    @commands.command(aliases=['listacp'])
    @commands.guild_only()
    async def listcp(self, ctx):

        dictCopypasts = dict(sorted(self.bot.dictCopypasts.items()))

        limitRangeCopypastDisplayInDiscord = 24
        beginLimitRangeCopypastDisplayInDiscord = 0
        listEmbedsCopypasts = []
        quantEmbedsCreates = math.ceil(len(dictCopypasts.keys()) / 25)

        for el in range(quantEmbedsCreates):

            listEmbedsCopypasts.append(discord.Embed(
                description='**Copypastas list**', colour=ctx.author.colour, timestamp=ctx.message.created_at))

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


    # Command to add new copypast
    @commands.command()
    @commands.guild_only()
    async def addcp(self, ctx, nameCP, *, textCP):

        if len(textCP) < 10:
            await ctx.send("The copypasta length must be at least 10 characters long.")
        
        else:

            reservedWordsFromOtherCommands = list(self.bot.all_commands.keys())

            self.updateVarAliasesCopypasts()

            if nameCP not in self.bot.aliasesCopypasts and nameCP not in reservedWordsFromOtherCommands:

                data = base64.b64encode(bytes(textCP, 'utf-8'))
                copypastAddRow = nameCP + "," + data.decode() + "," + str(ctx.message.author.id) + "\n"

                with open(self.bot.pathToCSVCopypastas, 'a') as fd:
                    fd.write(copypastAddRow)

                await ctx.send("**Added.**")

                # update aliases after add new copypast
                self.update_aliases(self._copypasta, [nameCP], "update")

            else:
                await ctx.send("This copypasta **already exists** or used a **reserved name from another command**.")
    

    # Handle Missing Argument for addcp
    @addcp.error
    async def addcp_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("One argument was missing.\nExample: -addcp __test__ __this is example test__.")
            ctx.handled_in_local = True


    # Command to delete a copypast
    @commands.command()
    @commands.guild_only()
    async def deletecp(self, ctx, nameCP: str):

        df = pd.read_csv(self.bot.pathToCSVCopypastas)

        if nameCP not in df.nameCP.values:
            await ctx.send("This copypasta does not exist.")

        else:
            for x in range(len(df.nameCP)):
                if nameCP == df.nameCP[x]:
                    if ctx.message.author.id != int(df.userWhoAdded[x]):
                        await ctx.send("You can only remove the ones you've added.")

                    else:
                        newDF = df.drop(df.index[x])

                        # Remove old csv
                        os.remove(self.bot.pathToCSVCopypastas)

                        # Save new csv
                        newDF.to_csv(self.bot.pathToCSVCopypastas, encoding='utf-8', index=False)

                        await ctx.send(f"The copypasta `{nameCP}` has been deleted.")

                        self.update_aliases(self._copypasta, nameCP, action="remove")
                        self.updateVarAliasesCopypasts()
    

    # Handle Missing Argument for deletecp
    @deletecp.error
    async def deletecp_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot the copypasta name. Ex: `-deletecp test`.")
            ctx.handled_in_local = True


def setup(bot):
    bot.add_cog(CopypastaCommands(bot))