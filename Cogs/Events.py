#!/bin/bash/python3
#coding: utf-8

import sys
import aiohttp
import discord
from datetime import datetime
from discord.ext import commands

# Local import
sys.path.append("..")
from Utils.getfiles import getJsonData


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

        to_send = next((
            chan for chan in sorted(guild.channels, key=lambda x: x.position)
            if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)
        ), None)

        if to_send:
            await to_send.send("Hello, my prefix is: **-**\nUse -help to see commands.")
        
        print(f"---- New guild join ----\nServer: {guild.name}.\nOwner: {guild.owner}\n")
    

    async def createLog(self, ctx):

        if not isinstance(ctx.channel, discord.channel.DMChannel):
                
            datetimeCommandInvoked = str(datetime.now().strftime('%d/%m/%Y - %H:%M:%S'))
            serverCommandInvoked = str(ctx.message.guild)
            serverIdCommandInvoked = str(ctx.message.guild.id)
            authorCommandInvoked = str(ctx.message.author)
            authorIdCommandInvoked =  str(ctx.message.author.id)

            embedLog = discord.Embed()

            embedLog.colour = discord.Colour(0x3CB043)

            if ctx.invoked_with not in list(self.bot.all_commands.keys()):
                embedLog.colour = discord.Colour(0xFF0000)

            embedLog.set_thumbnail(url=ctx.author.avatar_url)
            embedLog.add_field(name='**Command**', value=f"{ctx.message.clean_content}", inline=False)
            embedLog.add_field(name='**Server**', value=f"{serverCommandInvoked}")
            embedLog.add_field(name='**Server ID**', value=f"{serverIdCommandInvoked}")
            embedLog.add_field(name='**Date/Time**', value=f"{datetimeCommandInvoked}", inline=False)
            embedLog.add_field(name='**User**', value=str(authorCommandInvoked))
            embedLog.add_field(name='**User ID**', value=f"{authorIdCommandInvoked}")
            embedLog.add_field(name='**Channel**', value=f"{ctx.message.channel.name}", inline=False)

            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.partial(
                id=self.bot.dataConfiguration["webhook_id"],
                token=self.bot.dataConfiguration["webhook_token"],
                adapter=discord.AsyncWebhookAdapter(session)
            )
                await webhook.send(embed=embedLog)


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

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error, delete_after=1.0)

        elif isinstance(error, commands.CommandNotFound):
            await self.createLog(ctx)
            return
        
        elif isinstance(error, commands.NoPrivateMessage):
            return
        
        else:
            print('\n--- Unhandled error for the user - To see the full error, uncomment (remove "#") from line 115 in Cogs.Events.py ---')
            print(str(ctx.message.guild) + " - ID: " + str(ctx.message.guild.id))
            print("    " + str(ctx.message.author) + " - ID: " + str(ctx.message.author.id))
            print("        Command: " + ctx.invoked_with + " -> Error: " + str(error) + "\n")
            
            raise(error)


def setup(bot):
    bot.add_cog(Events(bot))