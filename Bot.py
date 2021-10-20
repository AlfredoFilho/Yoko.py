#!/bin/bash/python3
#coding: utf-8

import os
import sys
import discord
from pathlib import Path
from discord.ext import commands
from discord_components import DiscordComponents

# Local import
from Modules.Trie import Trie
from Modules.GetFiles import getJsonData, getDictFromCsv


# Create tmp folder if not exists
Path("tmp").mkdir(parents=True, exist_ok=True)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='-', help_command=None, intents=intents)
DiscordComponents(bot)

# Set some variables to use in other commands
bot.pathToCSVCopypastas = "files/DataCopypast.csv"
bot.pathToJSONHelpDescriptions = "files/HelpDescriptions.json"
bot.dataConfiguration = getJsonData("configuration.json")
bot.AllWordsPortuguese = Trie()
bot.startpingTasks = {}

# Get all words in files/AllPortugueseWords.txt for use in command "word" (Cogs.SubtitlesCommands)
with open('files/AllPortugueseWords.txt', 'r', encoding='utf-8') as fileWords:
    lines = fileWords.readlines()

    for word in lines:
        bot.AllWordsPortuguese.add(word.strip())

# Check that all configs in configuration.json have been filled
for key in bot.dataConfiguration.keys():
    if not bot.dataConfiguration[key]:
        print(f"Please, fill the required field -> {key} <- in configuration.json for all commands to work.")
        print("\nToken in https://discord.com/developers/applications")
        print("To get the other data, activate the Developer Mode and right click on your profile or channel.\n---- User Settings > Advanced > Developer Mode")
        sys.exit()

# Load Cogs
for file in sorted(os.listdir("Cogs")):
    if file.endswith(".py"):   

        name = file[:-3]
        bot.load_extension(f"Cogs.{name}")

        print(f"Cog {name} loaded")

bot.run(bot.dataConfiguration["token"])