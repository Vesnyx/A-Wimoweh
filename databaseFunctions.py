import csv
from trakt import Trakt
import jsonpickle as json

def databaseParser():
    print("Make sure the tsv is in the same directory.")
    with open('data.tsv', encoding='utf-8') as databaseInput, open('idList.txt', 'a') as outputFile:
        databaseInput = csv.reader(databaseInput, delimiter = '\t')
        for row in databaseInput:
            if(row[1] == "tvSeries"):
                outputFile.write(row[0] + '\n')
    print("Parsing copmleted.")

def traktData( file ):
    data = []
    with open(file, 'r') as idList, open('traktData.txt', 'a') as traktOutput, open('failed.txt', 'a') as failedOutput:
        for id in idList:
            print("Getting data for " + id.strip('\n'))
            dataLookup = Trakt['search'].lookup(id.strip('\n'), media = 'show', extended = 'full', service = 'imdb')
            if dataLookup is not None:
                data.append(dataLookup)
            else:
                failedOutput.write(id)
        traktOutput.write(json.encode(data))
        