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


def getTimeStartLine(line):
    '''
    Example:
    Dialogue: 10,0:03:17.93,0:03:21.26,Default,,0,0,0,,

    Return:
    time: 0:03:17.93
    '''

    line = line.split(",")
    time = line[1]

    return time


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
            description="Lembrete: Esse comando verifica os style **Default** e **Italics**",
            colour=discord.Colour(0xFFFF00)
        )

        await ctx.reply(embed=embedFile)
        await ctx.send(file=f)

        os.remove(pathToOriginalFile)
        os.remove(pathToNewFile)


async def cleanNCommand(ctx):

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


async def punctuationCommand(ctx):
    
    punctuation = ['"','?','!','...','.',',','…',':','“','”', '-', '—', '–']

    if not ctx.message.attachments:
        await ctx.send("Não encontrei um arquivo na sua mensagem.\nEnvie o arquivo juntamente com o comando.")

    else:

        urlFileFromDiscord = ctx.message.attachments[-1].url

        pathToNewFile = "tmp/punctuation-" + str(random.randint(100000, 1000000)) + ".txt"
        pathToOriginalFile = "tmp/texts-" + str(random.randint(100000, 1000000)) + ".txt"

        myfile = requests.get(urlFileFromDiscord, allow_redirects=True)
        open(pathToOriginalFile, 'wb').write(myfile.content)

        countLineWithoutPunctuation = 0

        with codecs.open(pathToOriginalFile, "r", encoding="utf8") as readOriginalFile:
            linesOriginalFile = readOriginalFile.readlines()

            with codecs.open(pathToNewFile, "w", encoding="utf8") as writeNewFile:
                for i in range(len(linesOriginalFile)):
                    line = linesOriginalFile[i]
                    if 'Dialogue' in line:
                        if 'Default' in line or 'Italics' in line:
                            
                            beforeNineComman, afterNineComman = splitNineComman(line)

                            lineWithoutTags = cleanTags(afterNineComman.strip())

                            # Check if last character is punctuation
                            if lineWithoutTags[-1] not in punctuation:
                                
                                countLineWithoutPunctuation += 1
                                
                                nextLine = linesOriginalFile[i + 1]

                                if 'Default' in line or 'Italics' in nextLine:
                                    
                                    nextLineBeforeNineComman, nextLineAfterNineComman = splitNineComman(nextLine)

                                    timeLine = getTimeStartLine(beforeNineComman)
                                    timeNextLine = getTimeStartLine(nextLineBeforeNineComman)

                                    contentLine = "\nLinha sem: " + timeLine + " - " + afterNineComman
                                    contentNextLine = "Próx linha: " + timeNextLine + " - " + nextLineAfterNineComman

                                    writeNewFile.write(contentLine)
                                    writeNewFile.write(contentNextLine)
                                
                                else:
                                    contentLine = "\nLinha sem: " + timeLine + " - " + afterNineComman
                                    writeNewFile.write(contentLine)

            writeNewFile.close()
        readOriginalFile.close()

        f = discord.File(pathToNewFile, filename="Linhas_Sem_Ponto.txt")
        embedFile = discord.Embed(
            title='Linhas sem pontuação no final',
            description = '''
            Número de linhas sem pontuação: **''' + str(countLineWithoutPunctuation)+ '**' + '''
            Lembrete: Esse comando verifica os style **Default** e **Italics**''',
            colour=discord.Colour(0xFFFF00)
        )

        await ctx.reply(embed=embedFile)
        await ctx.send(file=f)

        os.remove(pathToOriginalFile)
        os.remove(pathToNewFile)


async def cleanCommand(ctx):

    if not ctx.message.attachments:
        await ctx.send("Não encontrei um arquivo na sua mensagem.\nEnvie o arquivo juntamente com o comando.")

    else:

        urlFileFromDiscord = ctx.message.attachments[-1].url

        pathToNewFile = "tmp/clean-" + str(random.randint(100000, 1000000)) + ".txt"
        pathToOriginalFile = "tmp/texts-" + str(random.randint(100000, 1000000)) + ".txt"

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

                            writeNewFile.write(cleanLine)

            writeNewFile.close()
        readOriginalFile.close()

        f = discord.File(pathToNewFile, filename="Legenda_Clean.txt")
        embedFile = discord.Embed(
            title='Só o texto dos style Default e Italics',
            description="Lembrete: Esse comando verifica os style **Default** e **Italics**",
            colour=discord.Colour(0xFFFF00)
        )

        await ctx.reply(embed=embedFile)
        await ctx.send(file=f)

        os.remove(pathToOriginalFile)
        os.remove(pathToNewFile)

async def wordCommand(ctx, AllWordsPortuguese):

    await ctx.send("Teste")