import csv


class Round:
    roundNo = 0

    def __init__(self, delay, buildDelay, name, enemies):
        Round.roundNo += 1  # What round is it
        self.delay = int(delay)  # Time between enemies
        self.enemyList = enemies
        self.buildTime = int(buildDelay)  # Delay before round starts
        self.name = name
        self.nextEnemy = self.buildTime

    def update(self, ticks):
        self.nextEnemy -= ticks
        if self.nextEnemy < 1 and len(self.enemyList) > 0:
            self.nextEnemy = self.delay
            return self.enemyList.pop(0)
        else:
            return None


def get_next_round():  # Get the next round from csv
    with open('rounds.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i in range(Round.roundNo + 1):  # Get to correct line
            csvreader.__next__()
        row = csvreader.__next__()
        delay = row.pop(0)
        buildDelay = row.pop(0)
        name = row.pop(0)
        # make list out of the remaining fields
        enemyList = [i for i in row if i != '']
    return Round(delay, buildDelay, name, enemyList)
