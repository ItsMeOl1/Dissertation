import csv
with open('rounds.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    print(list(csvreader))
