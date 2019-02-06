import csv
import sys
#from trakt import Trakt
import jsonpickle as json
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

def databaseParser():
    print("Make sure the tsv is in the same directory.")
    with open('data.tsv', encoding = 'utf-8') as databaseInput, open('idList.tsv', 'a') as outputFile:
        databaseInput = csv.reader(databaseInput, delimiter = '\t')
        outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
        for row in databaseInput:
            if(row[1] == "tvSeries"):
                outputWriter.writerow(row)
    print("Parsing completed.")

def traktData( file ):
    #data = []
    with open(file, 'r') as idList, open('traktData.txt', 'a') as traktOutput, open('failed.txt', 'a') as failedOutput:
        for id in idList:
            print("Getting data for " + id.strip('\n'))
            dataLookup = Trakt['search'].lookup(id.strip('\n'), media = 'show', extended = 'full', service = 'imdb')
            if dataLookup is not None:
                print('Data found for ' + id.strip('\n') + '\r')
                traktOutput.write(json.encode(dataLookup) + '\n')
                #data.append(dataLookup)
            else:
                print('No data found for ' + id.strip('\n') + '\r')
                failedOutput.write(id)
        #traktOutput.write(json.encode(data))

def traktDataConverter( file , outputFileName):
    with open(file, 'r') as toConvert, open( outputFileName + '.txt', 'a') as outputFile:
        outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
        outputWriter.writerow(['species', 'clade', 'ts', 'te'])
        iterator = 0
        for line in toConvert:
            data = json.decode(line.strip('\n'))
            print(line)
            outputWriter.writerow(['0', iterator ])
            iterator += 1
            
def imdbDataConverter( file, outputFileName ):
    with open(file, 'r') as toConvert, open( outputFileName + '.txt', 'a' ) as outputFile:
        toConvert = csv.reader(toConvert, delimiter = '\t')
        outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
        outputWriter.writerow(['species', 'clade', 'ts', 'te'])
        iterator = 0
        for line in toConvert:
            outputWriter.writerow(['0', iterator, line[5], line[6]])
            iterator += 1
    print("Parsing completed.")

    
def sortDatabase( akasData, basicsData, region, type ):
    with open(akasData, 'r', encoding = "utf-8") as largeData, open(basicsData, 'r', encoding = "utf-8") as basicData, open('sortedRegion.txt', 'a') as outputFile:
        largeData = csv.reader(largeData, delimiter = '\t')
        basicData = csv.reader(basicData, delimiter = '\t')
        outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
        goodType = []
        goodRegion = []
        for row in largeData:
            if(row[1] == type):
                goodType.append(row)
        print("Finished parsing first file.")
        for row in basicData:
            if(row[3] == region):
                goodRegion.append(row[0])
        print("Finished parsing second file.")
        for video in goodType:
            if video[0] in goodRegion:
                outputWriter.writerow(video)
                goodRegion.remove(video[0])
        print("Sorted")
    
def getGenres( file ):
    genres = []
    with open( file, 'r', encoding = 'utf-8' ) as databaseInput:
        databaseInput = csv.reader(databaseInput, delimiter = '\t')
        for row in databaseInput:
            if(row[-1] != '\\N'):
                tempGenres = row[-1].split(',')
                for genre in tempGenres:
                    if genre not in genres:
                        genres.append(genre)
    return genres
    
def sortGenres( file ):
    genres = ['Documentary', 'Short', 'Animation', 'Comedy', 'Romance', 'Sport', 'News', 'Drama', 'Fantasy', 'Horror', 'Biography', 'Music', 'War', 'Crime', 'Western', 'Family', 'Adventure', 'History', 'Sci-Fi', 'Action', 'Mystery', 'Thriller', 'Musical', 'Film-Noir', 'Game-Show', 'Talk-Show', 'Reality-TV', 'Adult']
    for genre in genres:
        with open('genres/' + genre + '.tsv', 'a') as outputFile:
            outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
            with open( file, 'r') as databaseInput:
                databaseInput = csv.reader(databaseInput, delimiter = '\t')
                for row in databaseInput:
                    if(genre in row[-1]):
                        outputWriter.writerow(row)