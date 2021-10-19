#!/bin/bash/python3
#coding: utf-8

import sys
import discord
from datetime import datetime
from discord.ext import commands

# Local import
sys.path.append("..")
from Modules.GetFiles import getJsonData


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):

        print('---------------------')
        print('       ONLINE        ')
        print('---------------------\n')

        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('-help'))


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        
        channelLog = self.bot.get_channel(int(self.dataConfiguration["channelIdForLogCommands"]))
        
        await channelLog.send(f"---- New guild join ----\n **Server:** {guild.name}.\n **Owner:** <@{guild.owner_id}>")
    

    async def createLog(self, ctx):

        if not isinstance(ctx.channel, discord.channel.DMChannel):
                
            commandInvoked = ''
            datetimeCommandInvoked = str(datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
            serverCommandInvoked = str(ctx.message.guild)
            serverIdCommandInvoked = str(ctx.message.guild.id)
            authorCommandInvoked = str(ctx.message.author)
            authorIdCommandInvoked =  str(ctx.message.author.id)

            if len(ctx.args) > 2:
                commandInvoked = '-' + str(ctx.invoked_with) + " " + str(ctx.args[2])
            else:
                commandInvoked = '-' + str(ctx.invoked_with)

            embedLog = discord.Embed()

            channelLog = self.bot.get_channel(int(self.bot.dataConfiguration["channelIdForLogCommands"]))
            embedLog.colour = discord.Colour(0x3CB043)

            if ctx.invoked_with not in list(self.bot.all_commands.keys()):
                channelLog = self.bot.get_channel(int(self.bot.dataConfiguration["channelIdForLogCommandsNotFound"]))
                embedLog.colour = discord.Colour(0xFF0000)

            embedLog.set_thumbnail(url=ctx.author.avatar_url)
            embedLog.add_field(name='**Command**', value=f"{commandInvoked}", inline=False)
            embedLog.add_field(name='**Server**', value=f"{serverCommandInvoked}")
            embedLog.add_field(name='**Server ID**', value=f"{serverIdCommandInvoked}")
            embedLog.add_field(name='**Date/Time**', value=f"{datetimeCommandInvoked}", inline=False)
            embedLog.add_field(name='**User**', value=str(authorCommandInvoked))
            embedLog.add_field(name='**User ID**', value=f"{authorIdCommandInvoked}")
            embedLog.add_field(name='**Channel**', value=f"{ctx.message.channel.name}", inline=False)

            await channelLog.send(embed=embedLog)


    # Event for every command used
    @commands.Cog.listener()
    async def on_command(self, ctx):

        await self.createLog(ctx)


    # Errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx, "handled_in_local"):
            if ctx.handled_in_local == True:
                return

        elif isinstance(error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            await ctx.send(error)
            return

        elif isinstance(error, commands.CommandNotFound):
            await self.createLog(ctx)
            return
        
        elif isinstance(error, commands.NoPrivateMessage):
            return
        
        else:
            print('--- Unhandled error for the user - To see the full error, uncomment (remove "#") from line 107 in Cogs.Events.py ---')
            print(str(ctx.message.guild) + " - ID: " + str(ctx.message.guild.id))
            print("    " + str(ctx.message.author) + " - ID: " + str(ctx.message.author.id))
            print("        Command: " + ctx.invoked_with + " -> Error: " + str(error) + "\n")
            
            # raise(error)


def setup(bot):
    bot.add_cog(Events(bot))