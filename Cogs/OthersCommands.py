#!/bin/bash/python3
#coding: utf-8

import sys
import asyncio
import discord
import platform
from discord_components import *
from discord.ext import commands, tasks


class OthersCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    # Command ping - latency the bot
    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):

        latencyBot = round(self.bot.latency * 1000)

        await ctx.send('**Hey!** _' + str(latencyBot) + 'ms_')


    # Command purge - delete messages
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    async def purge(self, ctx, quant: int):

        quant = quant + 1

        if quant > 100:
            quant = 100

        channelToDeleteMessages = ctx.message.channel

        messagesDel = await channelToDeleteMessages.history(limit=quant).flatten()

        if len(messagesDel) == 0:
            await ctx.send("There are no messages to be deleted.", delete_after=3.0)
        
        else:
            try:
                await channelToDeleteMessages.delete_messages(messagesDel)
                await ctx.send(f"Deleted **{len(messagesDel) - 1}** messages.", delete_after=2.0)
            
            except discord.errors.HTTPException:
                await ctx.send("A bot can only delete messages up to 14 days ago.", delete_after=5.0)


    # Handle Missing Argument for purge
    @purge.error
    async def purge_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("The required argument `quant` is missing.")
            ctx.handled_in_local = True


    # Command stats - infos bot
    @commands.command()
    @commands.guild_only()
    async def stats(self, ctx):

        # infoBot = await bot.application_info()

        pythonVersion = platform.python_version()
        discordPyVersion = discord.__version__

        embedStatus = discord.Embed(description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embedStatus.add_field(name='Bot Version', value='3.0 - 11/Oct/2021')
        embedStatus.add_field(name='Python Version', value=pythonVersion)
        embedStatus.add_field(name='Discord.Py Version', value=discordPyVersion)

        embedStatus.set_footer(text=f"{self.bot.user.name}")
        embedStatus.set_author(name='Yoko - Stats', icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embedStatus)
        

    def getInfosFromCtx(self, ctx):

        serverName = ctx.message.guild.name
        serverId = ctx.message.guild.id
        channelName = ctx.message.channel.name
        channelId = ctx.message.channel.id

        return str(serverName), str(serverId), str(channelName), str(channelId)


    async def addTaskFromServer(self, ctx, member, task, contentMessage):

        serverName, serverId, channelName, channelId = self.getInfosFromCtx(ctx)

        self.bot.startpingTasks["servers"][serverId] = {}
        self.bot.startpingTasks["servers"][serverId]["serverName"] = serverName
        self.bot.startpingTasks["servers"][serverId]["channels"] = {}

        await self.addTaskFromChannel(ctx, member, task, contentMessage)


    async def addTaskFromChannel(self, ctx, member, task, contentMessage):

        serverName, serverId, channelName, channelId = self.getInfosFromCtx(ctx)

        self.bot.startpingTasks["servers"][serverId]["channels"][channelId] = {}
        self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["channelName"] = channelName
        self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"] = {}

        await self.addTaskFromUser(ctx, member, task, contentMessage)


    async def addTaskFromUser(self, ctx, member, task, contentMessage):

        serverName, serverId, channelName, channelId = self.getInfosFromCtx(ctx)
        userName = member.name
        userId = str(member.id)

        self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"][userId] = {}
        self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"][userId]["userName"] = userName
        self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"][userId]["task"] = task

        await ctx.send("**30sg** delay. To disable: **-endping**")
        task.start(ctx, member, contentMessage)


    async def addTask(self, ctx, member, locationForAdd, taskForAdd, contentMessage):
        
        if locationForAdd == "user":

            await self.addTaskFromUser(ctx, member, taskForAdd, contentMessage)
        
        if locationForAdd == "channel":

            await self.addTaskFromChannel(ctx, member, taskForAdd, contentMessage)

        if locationForAdd == "server":

            if not self.bot.startpingTasks:
                self.bot.startpingTasks["servers"] = {}
            await self.addTaskFromServer(ctx, member, taskForAdd, contentMessage)


    async def loopPing(self, ctx, member, contentMessage):

        await ctx.send(f"<@{member.id}> {contentMessage}")


    async def task_generator(self, ctx, member, contentMessage):
        
        serverName, serverId, channelName, channelId = self.getInfosFromCtx(ctx)
        userId = member.id

        t = tasks.loop(seconds=30)(self.loopPing)

        if self.bot.startpingTasks:
            if serverId in self.bot.startpingTasks["servers"]:
                if channelId in self.bot.startpingTasks["servers"][serverId]["channels"]:
                    
                    listWithUserAlreadyCreated = [int(x) for x in self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"].keys()]
                    if int(userId) in listWithUserAlreadyCreated:
                        await ctx.send("It has already been created for that person on this channel.")
                    else:
                        await self.addTask(ctx, member, "user", t, contentMessage)
                else:
                    await self.addTask(ctx, member, "channel", t, contentMessage)
            else:
                await self.addTask(ctx, member, "server", t, contentMessage)
        else:
            await self.addTask(ctx, member, "server", t, contentMessage)


    @commands.command()
    @commands.guild_only()
    async def startping(self, ctx, member: discord.Member, *, contentMessage="?"):

        if member.id == self.bot.user.id:
            await ctx.send(f"You can't create one for {self.bot.user.name} xD.")

        elif ctx.message.author.id == member.id:
            await ctx.send("You cannot create one for yourself.")
        
        else:
            await self.task_generator(ctx, member, contentMessage)
    

    @startping.error
    async def startpingError(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot some argument. Example: `-startping @member good morning`")
            ctx.handled_in_local = True


    async def deleteTask(self, ctx):

        serverName, serverId, channelName, channelId = self.getInfosFromCtx(ctx)

        usersForDelete = self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"]
        channelsForDelete = self.bot.startpingTasks["servers"][serverId]["channels"]

        dropdownEndping = await ctx.send(
                    "Select someone!",
                    components=[
                        Select(
                            placeholder="Options",
                            options=[SelectOption(label=str(usersForDelete[x]["userName"]), value=str(x)) for x in usersForDelete.keys()
                                    ],
                            custom_id="select1",
                        )
                    ],
                )

        try:
            interaction = await self.bot.wait_for(
                "select_option", check=lambda res: res.message.id == dropdownEndping.id, timeout=10
            )

            idUserFromTask = interaction.values[0]

            if str(interaction.user.id) != idUserFromTask:
                
                userSelected = self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"][str(idUserFromTask)]
                
                await interaction.respond(type=6)
                await dropdownEndping.edit(content=f"Desativado para {userSelected['userName']}.", components=[])

                # Cancel task
                self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"][str(idUserFromTask)]["task"].cancel()

                if len(usersForDelete.keys()) > 1:
                    del self.bot.startpingTasks["servers"][serverId]["channels"][channelId]["users"][str(idUserFromTask)]
                
                else:
                    if len(channelsForDelete.keys()) == 1 and len(usersForDelete.keys()) == 1:
                        del self.bot.startpingTasks["servers"][serverId]
                    else:
                        del self.bot.startpingTasks["servers"][serverId]["channels"][channelId]

            else:
                await ctx.send(f"{interaction.user.name}, you cannot disable it for yourself.")
                await dropdownEndping.delete()

        except asyncio.TimeoutError:
            await ctx.send('Timed Out!')
            await dropdownEndping.delete()


    @commands.command()
    @commands.guild_only()
    async def endping(self, ctx):

        if not self.bot.startpingTasks:
            await ctx.send("There is no **-startping** running on this channel.")
        
        else:
            serverName, serverId, channelName, channelId = self.getInfosFromCtx(ctx)
            
            if serverId in self.bot.startpingTasks["servers"]:
                if channelId in self.bot.startpingTasks["servers"][serverId]["channels"]:
                    await self.deleteTask(ctx)
                else:
                    await ctx.send("There is no **-startping** running on this channel.")
            else:
                await ctx.send("There is no **-startping** running on this channel.") 


def setup(bot):
    bot.add_cog(OthersCommands(bot))