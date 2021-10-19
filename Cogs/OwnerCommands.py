#!/bin/bash/python3
#coding: utf-8

from discord.ext import commands


class OwnerCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # Command to take the bot off a server
    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def leave(self, ctx, guild_id):

        await self.bot.get_guild(int(guild_id)).leave()
        await ctx.send(f"I left: {guild_id}")


    # Command to shutdown the bot
    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def shutdown(self, ctx):

        embedShutdown = discord.Embed(
            description = '**Shutdown...**',
            colour = discord.Colour(0xFF0000)
        )

        await ctx.send(embed = embedShutdown)
        await ctx.bot.logout()


    # Print all servers and owners (in terminal / cmd)
    @commands.command()
    @commands.is_owner()
    @commands.guild_only()
    async def listservers(self, ctx):

        listServers = []

        for activeServer in self.bot.guilds:

            listServers.append([activeServer.name, activeServer.id, activeServer.owner, activeServer.owner_id])

        listServers.sort(key = lambda x:x[0])
        maxlenServerName = len(max([x[0] for x in listServers], key=len))
        maxlenServerOwnerName = len(max([str(x[2]) for x in listServers], key=len))

        for el in range(len(listServers)):
            listServers[el][0] = listServers[el][0].ljust(maxlenServerName, "-")
            listServers[el][2] = str(listServers[el][2]).ljust(maxlenServerOwnerName, "-")

        serversAndOwner = ""

        for el in listServers:
            serverName = el[0].title()
            serverID = str(el[1])
            serverOwner = el[2]
            serverOwnerID = str(el[3])

            serversAndOwner = serversAndOwner + "Server name: " + serverName + " Server ID: " + serverID + " <-> Owner tag: " + serverOwner + " Owner ID: " + serverOwnerID + "\n"

        print(serversAndOwner)


def setup(bot):
    bot.add_cog(OwnerCommands(bot))