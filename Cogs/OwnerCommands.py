#!/bin/bash/python3
#coding: utf-8

import os
import pprint
from discord.ext import commands


class OwnerCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # Command to take the bot off a server
    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def leave(self, ctx, guild_id):

        await self.bot.get_guild(int(guild_id)).leave()
        await ctx.send(f"I left: {guild_id}")


    # Command to shutdown the bot
    @commands.command(hidden=True)
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
    @commands.command(hidden=True)
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
    

    # Print tasks running on -startping command
    @commands.command(hidden=True)
    @commands.is_owner()
    async def printTasks(self, ctx):

        pprint.pprint(self.bot.startpingTasks)


    # Reload Cogs
    @commands.command(hidden=True)
    @commands.is_owner()
    async def reloadcogs(self, ctx):
        
        # Cancel all tasks from -startping command before reloading Cogs
        if self.bot.startpingTasks:
            if self.bot.startpingTasks["servers"]:
                for server in self.bot.startpingTasks["servers"].keys():
                    if self.bot.startpingTasks["servers"][server]:
                        for channel in self.bot.startpingTasks["servers"][server]["channels"].keys():
                            if self.bot.startpingTasks["servers"][server]["channels"][channel]:
                                if self.bot.startpingTasks["servers"][server]["channels"][channel]["users"]:
                                    for user in self.bot.startpingTasks["servers"][server]["channels"][channel]["users"].keys():

                                        # Cancel task
                                        self.bot.startpingTasks["servers"][server]["channels"][channel]["users"][user]["task"].cancel()

                                        channelToSendTheNotice = self.bot.get_channel(int(channel))
                                        await channelToSendTheNotice.send("The **-startping** on this channel was disabled because the Bot restarted.")
        
        self.bot.startpingTasks = {}

        # Clear terminal / cmd
        os.system('cls' if os.name == 'nt' else 'clear')

        # Reload
        for file in sorted(os.listdir("Cogs")):
            if file.endswith(".py"): 

                name = file[:-3]
                self.bot.unload_extension(f"Cogs.{name}")
                self.bot.load_extension(f"Cogs.{name}")

                print(f"Cog {name} reloaded")
        
        print('---------------------')
        print('       ONLINE        ')
        print('---------------------\n')


def setup(bot):
    bot.add_cog(OwnerCommands(bot))