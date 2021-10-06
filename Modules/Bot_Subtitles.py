#!/bin/bash/python3
#coding: utf-8

import re
import os
import random
import codecs
import discord
import requests


def splitNineComman(line):
    '''
    Example:
    Dialogue: 10,0:03:17.93,0:03:21.26,Default,,0,0,0,,This is an example of {\i1}subtitle{\i0} .ass

    Return:
    beforeNineComman: Dialogue: 10,0:03:17.93,0:03:21.26,Default,,0,0,0,,
    afterNineComman: This is an example of {\i1}subtitle{\i0} .ass
    '''

    line = line.split(",")

    beforeNineComman = line[:9]
    beforeNineComman = ",".join(beforeNineComman) + ","

    afterNineComman = line[9:]

    if len(afterNineComman) > 1:
        afterNineComman = ",".join(afterNineComman)

    else:
        afterNineComman = afterNineComman[0]

    return beforeNineComman, afterNineComman


def cleanTags(line):
    '''
    Example:
    This is an example of {\i1}subtitle{\i0} .ass

    Return:
    This is an example of subtitle .ass
    '''

    if '{' in line:
        line = re.sub(r"{[^}]+}", r"", line)
    
    return line


def cleanNewLineAndMultipleSpace(line):
    '''
    Example:
    This is an example   of {\i1}subtitle{\i0} .ass

    Return:
    This is an example of {\i1}subtitle{\i0} .ass
    '''

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

                            beforeNineComman, afterNineComman = splitNineComman(line)
                            cleanLine = cleanNewLineAndMultipleSpace(afterNineComman)
                            cleanLine = cleanTags(cleanLine)

                            for word in wordsForVerification:
                                if word in cleanLine:
                                    cleanLine = "- " + cleanLine.replace(word, '*' + word + '*')

                                    writeNewFile.write(cleanLine)

            writeNewFile.close()
        readOriginalFile.close()

        f = discord.File(pathToNewFile, filename="crasepq.txt")
        embedFile = discord.Embed(
            title='Linhas com _crases_ e _porquês_',
            description="Lembrete: esse comando verifica os style **Default** e **Italics**",
            colour=discord.Colour(0xFFFF00)
        )

        await ctx.reply(embed=embedFile)
        await ctx.send(file=f)

        os.remove(pathToOriginalFile)
        os.remove(pathToNewFile)


async def cleanN(ctx):

    if not ctx.message.attachments:
        await ctx.send("Não encontrei um arquivo na sua mensagem.\nEnvie o arquivo juntamente com o comando.")

    else:

        urlFileFromDiscord = ctx.message.attachments[-1].url

        pathToNewFile = "tmp/cleanN-" + str(random.randint(100000, 1000000)) + ".txt"
        pathToOriginalFile = "tmp/texts-" + str(random.randint(100000, 1000000)) + ".txt"

        myfile = requests.get(urlFileFromDiscord, allow_redirects=True)
        open(pathToOriginalFile, 'wb').write(myfile.content)

        countLineChanges = 0

        with codecs.open(pathToOriginalFile, "r", encoding="utf8") as readOriginalFile:
            linesOriginalFile = readOriginalFile.readlines()

            with codecs.open(pathToNewFile, "w", encoding="utf8") as writeNewFile:
                for line in linesOriginalFile:
                    if 'Dialogue' in line:
                        if 'Default' in line or 'Italics' in line:

                            beforeNineComman, afterNineComman = splitNineComman(line)
                            cleanLine = cleanNewLineAndMultipleSpace(afterNineComman)

                            lineAfterChanges = beforeNineComman + cleanLine

                            if lineAfterChanges != line:
                                countLineChanges += 1

                            writeNewFile.write(lineAfterChanges)
                        
                        else:
                            writeNewFile.write(line)
                    else:
                        writeNewFile.write(line)

            writeNewFile.close()
        readOriginalFile.close()

        f = discord.File(pathToNewFile, filename="Legenda_Sem_N.ass")
        embedFile = discord.Embed(
                title = 'Legenda sem \\N e duplo espaço',
                description = '''
                Número de linhas alteradas: **''' + str(countLineChanges)+ '**' + '''
                 As alterações são feitas nos style **Default** e **Italics**''',
                colour = discord.Colour(0xFFFF00)
        )

        await ctx.reply(embed=embedFile)
        await ctx.send(file=f)

        os.remove(pathToOriginalFile)
        os.remove(pathToNewFile)