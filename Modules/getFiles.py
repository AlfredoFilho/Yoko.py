#!/bin/bash/python3
#coding: utf-8
import json
import pandas as pd


def getJsonData(pathToJsonFile):

    with open(pathToJsonFile) as json_data:
        jsonData = json.load(json_data)

    return jsonData


def getDictFromCsv(pathToCsv, nameKey, nameValue):
    
    df = pd.read_csv(pathToCsv)
    return pd.Series(df[nameValue].values,index=df[nameKey]).to_dict()