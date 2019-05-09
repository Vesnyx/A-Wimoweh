import csv
import sys
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
        
def readFileToDict( file ):
    data = {}
    for line in csv.reader( file, delimiter = '\t' ):
        data[line[0]] = line[1:]
    return data

# Test Function (serves no purpose now)
def databaseParser():
    print("Make sure the tsv is in the same directory.")
    with open('data.tsv', encoding = 'utf-8') as databaseInput, open('idList.tsv', 'a') as outputFile:
        databaseInput = csv.reader(databaseInput, delimiter = '\t')
        outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
        for row in databaseInput:
            if(row[1] == "tvSeries"):
                outputWriter.writerow(row)
    print("Parsing completed.")

# Takes in file of imdb id's to gather trakt data on all available shows (DO NOT USE)
def traktData( file ):
    with open(file, 'r') as idList, open('traktData.txt', 'a') as traktOutput, open('failed.txt', 'a') as failedOutput:
        for id in idList:
            print("Getting data for " + id.strip('\n'))
            dataLookup = Trakt['search'].lookup(id.strip('\n'), media = 'show', extended = 'full', service = 'imdb')
            if dataLookup is not None:
                print('Data found for ' + id.strip('\n') + '\r')
                traktOutput.write(json.encode(dataLookup) + '\n')
            else:
                print('No data found for ' + id.strip('\n') + '\r')
                failedOutput.write(id)

# Converts trakt to liteRate formatted data.
def traktDataConverter( file , outputFileName ):
    with open(file, 'r') as toConvert, open( outputFileName, 'a') as outputFile:
        outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
        outputWriter.writerow(['clade', 'species', 'ts', 'te'])
        iterator = 0
        for line in toConvert:
            data = json.decode(line.strip('\n'))
            print(line)
            outputWriter.writerow(['0', iterator ])
            iterator += 1
            
def imdbDataConverter( file, outputFileName, initialYear, finalYear ):
    with open(file, 'r') as toConvert, open( outputFileName, 'a' ) as outputFile:
        toConvert = csv.reader(toConvert, delimiter = '\t')
        outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
        outputWriter.writerow(['clade', 'species', 'ts', 'te'])
        iterator = 0
        for line in toConvert:
            if line[5] != "\\N" and int(line[5]) > initialYear and int(line[5]) < finalYear:
                if line[6] != "\\N":
                    outputWriter.writerow(['0', line[0], line[5], line[6]])
                else:
                    outputWriter.writerow(['0', line[0], line[5], finalYear])
            iterator += 1
    print("Parsing completed.")

# Function that takes in akas (Region) and title data to return a filtered set of shows based on region and type.
def sortDatabase( akasData, basicsData, region, type ):
    with open(akasData, 'r', encoding = "utf-8") as regionData, open(basicsData, 'r', encoding = "utf-8") as basicData, open('sortedRegion.txt', 'a') as outputFile:
        regionData = csv.reader(regionData, delimiter = '\t')
        basicData = csv.reader(basicData, delimiter = '\t')
        outputWriter = csv.writer(outputFile, delimiter = '\t', lineterminator = '\n')
        goodRegion = []
        for row in largeData:
            if(row[3] == region):
                goodRegion.append(row[0])
        print("Finished parsing akas file.")
        for row in basicData:
            if row[0] in goodRegion and row[1] == type:
                outputWriter.writerow(row)
                goodRegion.remove(row[0])
        print("Sorted")

# Function that returns all genres present in a title.basics.tsv file.    
def getGenres( file ):
    genres = []
    with open( file, 'r', encoding = 'utf-8' ) as databaseInput:
        databaseInput = csv.reader( databaseInput, delimiter = '\t' )
        for row in databaseInput:
            if(row[-1] != '\\N'):
                tempGenres = row[-1].split(',')
                for genre in tempGenres:
                    if genre not in genres:
                        genres.append( genre )
    return genres

# Function that sorts all shows into individual genre files (inclusive). May include redundant shows.    
def sortGenres( file ):
    genres = ['Documentary', 'Short', 'Animation', 'Comedy', 'Romance', 'Sport', 'News', 'Drama', 'Fantasy', 'Horror', 'Biography', 'Music', 'War', 'Crime', 'Western', 'Family', 'Adventure', 'History', 'Sci-Fi', 'Action', 'Mystery', 'Thriller', 'Musical', 'Film-Noir', 'Game-Show', 'Talk-Show', 'Reality-TV', 'Adult']
    for genre in genres:
        with open('genres/' + genre + '.tsv', 'a') as outputFile:
            outputWriter = csv.writer( outputFile, delimiter = '\t', lineterminator = '\n' )
            with open( file, 'r' ) as databaseInput:
                databaseInput = csv.reader( databaseInput, delimiter = '\t' )
                for row in databaseInput:
                    if(genre in row[-1]):
                        outputWriter.writerow( row )

# Function that sorts all shows into different files based on their genre combinations (non-inclusive).
def sortMultiGenres( file ):
    with open( file, 'r') as databaseInput:
        databaseInput = csv.reader( databaseInput, delimiter = '\t' )
        genreCombos = {}
        for row in databaseInput:
            if row[-1] in genreCombos:
                genreCombos[row[-1]].append( row )
            else:
                genreCombos[row[-1]] = [row]
        for genreCombo in genreCombos:
            with open( 'genreCombos/' + genreCombo.replace( ',', ' ' ) + '.tsv', 'a' ) as outputFile:
                outputWriter = csv.writer( outputFile, delimiter = '\t', lineterminator = '\n' )
                for show in genreCombos[genreCombo]:
                    outputWriter.writerow( show )

def dateSorter( file, outputFileName, year ):
    with open( file, 'r' ) as toConvert, open( outputFileName, 'a' ) as outputFile:
        toConvert = csv.reader( toConvert, delimiter = '\t' )
        outputWriter = csv.writer( outputFile, delimiter = '\t', lineterminator = '\n' )
        for line in toConvert:
            if line[0] == "clade":
                outputWriter.writerow(line)
            elif int(line[2]) < year:
                outputWriter.writerow(line)
    print("Parsing completed.")
    
def episodeRatingsCombiner( ratingsFileName, episodesFileName, outputFileName ):
    with open( ratingsFileName, 'r' ) as ratingsFile, open( episodesFileName, 'r' ) as episodesFile, open( outputFileName, 'a' ) as outputFile:
        ratingsFile = readFileToDict( ratingsFile )
        episodesFile = readFileToDict ( episodesFile )
        outputWriter = csv.writer( outputFile, delimiter = '\t', lineterminator = '\n' )
        for key in episodesFile:
            try:
                outputWriter.writerow((key, episodesFile[key][0], episodesFile[key][1], episodesFile[key][2], ratingsFile[key][0], ratingsFile[key][1]))
            except KeyError:
                outputWriter.writerow((key, episodesFile[key][0], episodesFile[key][1], episodesFile[key][2], '\\N', '\\N'))
    print("Parsing comleted.")