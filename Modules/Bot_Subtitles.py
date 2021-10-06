#!/bin/bash/python3
#coding: utf-8

import re
import os
import random
import codecs
import discord
import requests


def removeTrashContent(line):
    """
    Remove trash content

    Return: Only the text of line
    """

    line = line.split(",")
    line = line[9:]

    if len(line) > 1:
        line = ",".join(line)

    else:
        line = line[0]

    if '{' in line:
        line = re.sub(r"{[^}]+}", r"", line)
    if '\\N' in line:
        line = line.replace('\\N', ' ')
    if '   ' in line:
        line = line.replace('   ', ' ')
    if '  ' in line:
        line = line.replace('  ', ' ')

    return line


async def crasepqCommand(ctx):

    if not ctx.message.attachments:
        await ctx.send("Não encontrei um arquivo na sua mensagem.\nEnvie o arquivo juntamente com o comando.")

    else:

        urlFileFromDiscord = ctx.message.attachments[-1].url

        pathToNewFile = "tmp/crasePq-" + str(random.randint(100000, 1000000)) + ".txt"
        pathToOriginalFile = "tmp/texts-" + str(random.randint(100000, 1000000)) + ".txt"

        wordsForVerification = ['Por que', 'Por quê', 'Porque', 'Porquê',
                                'por que', 'por quê', 'porque', 'porquê', 'à', 'têm']

        myfile = requests.get(urlFileFromDiscord, allow_redirects=True)
        open(pathToOriginalFile, 'wb').write(myfile.content)

        with codecs.open(pathToOriginalFile, "r", encoding="utf8") as readOriginalFile:
            linesOriginalFile = readOriginalFile.readlines()

            with codecs.open(pathToNewFile, "w", encoding="utf8") as writeNewFile:
                for line in linesOriginalFile:
                    if 'Dialogue' in line:
                        if 'Default' in line or 'Italics' in line:

                            line = removeTrashContent(line)

                            for word in wordsForVerification:
                                if word in line:
                                    line = "- " + line.replace(word, '*' + word + '*')

                                    writeNewFile.write(line)

            writeNewFile.close()
        readOriginalFile.close()

        f = discord.File(pathToNewFile, filename="crasepq.txt")
        embedFile = discord.Embed(
            title='Linhas com _crases_ e _porquês_',
            description="Lembrete: esse comando verifica os style **Default** e **Italics**",
            colour=discord.Colour(0xFFFF00)
        )

        await ctx.reply(embed=embedFile)
        await ctx.channel.send(file=f)

        os.remove(pathToOriginalFile)
        os.remove(pathToNewFile)