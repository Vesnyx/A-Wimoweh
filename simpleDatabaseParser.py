import csv

print("Make sure the tsv is in the same directory.")
with open('data.tsv', encoding='utf-8') as databaseInput, open('idList.txt', 'a') as outputFile:
    databaseInput = csv.reader(databaseInput, delimiter = '\t')
    for row in databaseInput:
        if(row[1] == "tvSeries"):
            outputFile.write(row[0] + '\n')
print("Parsing copmleted.")