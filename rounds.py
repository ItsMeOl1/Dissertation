import csv

class Round:
    roundNo = 0
    def __init__(self, delay, buildDelay, name, enemies):
        Round.roundNo += 1
        self.delay = int(delay)
        self.enemyList = enemies
        self.buildTime = int(buildDelay)
        self.name = name
        self.nextEnemy = self.buildTime
    
    def update(self, ticks):
        self.nextEnemy -= ticks
        print(self.nextEnemy, bool(self.enemyList))
        if self.nextEnemy < 1 and len(self.enemyList) > 0:
            self.nextEnemy = self.delay
            return self.enemyList.pop(0)
        else:
            return None

def get_next_round():
    with open('rounds.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i in range(Round.roundNo + 1):
            csvreader.__next__()
        row = csvreader.__next__()
        delay = row.pop(0)
        buildDelay = row.pop(0)
        name = row.pop(0)
        enemyList = [i for i in row if i != '']
    return Round(delay, buildDelay, name, enemyList)
