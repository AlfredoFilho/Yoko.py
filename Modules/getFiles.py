#!/bin/bash/python3
#coding: utf-8
import json
import pandas as pd


def getJsonData(pathToJsonFile):

    with open(pathToJsonFile) as json_data:
        jsonData = json.load(json_data)

    return jsonData


def getDictFromCsv(pathToCsv):
    
    return pd.read_csv(pathToCsv, header=None, index_col=0, squeeze=True).to_dict()    