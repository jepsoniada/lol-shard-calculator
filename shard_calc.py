import time
start_time = time.time()
class Calcpart:
    def __init__(self, index, symbol):
        self.symbol = symbol
        self.index = index
    def symbolDisplay(self):
        return 1 if self.symbol else 0
    def __repr__(self):
        return f"({self.index} {self.symbolDisplay()})"

class CalcResult:
    def __init__(self, value, wayToGet):
        self.value = value
        self.wayToGet = [wayToGet]
    def __repr__(self):
        return f"{self.value} : {self.wayToGet}"

class OverallCalcResults:
    def __init__(self):
        self.banlist = []
        self.resultList = []
    def addResult(self, resultObj):
        if len(self.resultList) == 0:
            self.resultList.append(resultObj)
        else:
            anacc = 0
            for i, a in enumerate(self.resultList, start=0):
                if a.value == resultObj.value:
                    self.resultList[i].wayToGet.append(resultObj.wayToGet[0])
                    break
                else:
                    anacc += 1
            if anacc == len(self.resultList):
                self.resultList.append(resultObj)
    def uptadeResults(self, goal):
        for a in self.resultList:
            if a.value == goal:
                lsIHolder = list(range(len(self.resultList)))
                banindexes = []
                for b in lsIHolder:
                    if self.resultList[b].value != goal:
                        banindexes.append(b)
                        hold = self.resultList[b]
                        self.banlist.append(hold)
                for b in reversed(banindexes):
                    self.resultList.pop(b)
                break
    def displayConclusion(self, goal, dqa, dqv):
        optimalgoallist = []
        for a in self.resultList:
            if a.value == goal:
                lencheck = len(a.wayToGet[0])
                for b in a.wayToGet:
                    if len(b) == lencheck:
                        optimalgoallist.append(b)
                    else:
                        break
                print('optimal goal:\n', ',\n'.join(list(map(lambda n: ' '.join(n), optimalgoallist))))
                break
        if not optimalgoallist:
            if dqa:
                waitlist = []
                dqMarginLs = []
                for a in list(map(lambda a: goal-(a*50), range(1, dqv+1))):
                    if a >= 0:
                        dqMarginLs.append(a)
                    else:
                        break
                for a in dqMarginLs:
                    for b in self.resultList:
                        if a == b.value:
                            lencheck = len(b.wayToGet[0])
                            stack = []
                            for c in b.wayToGet:
                                if len(c) == lencheck:
                                    stack.append(c)
                                else:
                                    break
                            waitlist.append({f'with {(goal - a) // 50} daily quests': stack})
                if waitlist:
                    print(list(map(lambda a: f'{list(a.keys())[0]} :\n', waitlist))[0], list(map(lambda a: ",\n".join(list(map(lambda q: " ".join(q), list(a.values())[0]))), waitlist))[0])
            else:
                print("there's no way to achive your goal, sorry ::((")

# 450 +90 -270
# 1350 +270 -810
# 3150 +630 - 1890
# 4800 +960 -2880
# 6300 +1260 -3780
# 7800 +1560 -4680

class Main:
    def __init__(self, maxactions = 4, actionsbelow = 'y', shards = 450, gotoscore = 540, allowdq = 'y', dqv = 3):
        if allowdq == 'y':
            self.allowdq = True
        elif allowdq == 'n':
            self.allowdq = False
        else:
            raise ValueError('got sth else than "y" or "n" in allowdq')
        if actionsbelow == 'y':
            self.actionsbelow = True
        elif actionsbelow == 'n':
            self.actionsbelow = False
        else:
            raise ValueError('got sth else than "y" or "n" in actionsbelow')
        self.ocr = OverallCalcResults()
        self.add = [90, 270, 630, 960, 1260, 1560]
        self.remove = [450, 1350, 3150, 4800, 6300, 7800, 270, 810, 1890, 2880, 3780, 4680]
        self.maxactions = int(maxactions)
        self.shards = int(shards)
        self.gotoscore = int(gotoscore)
        self.dqv = int(dqv)
        self.calclist = []
        self.calcfill(self.maxactions)
        print('ab: ', self.actionsbelow, 'dq: ', self.allowdq)
    def calcfill(self, howmuch):
        self.calclist = [0 for a in range(howmuch)]
    def addResulter(self, resulte):
        # fullcalc = list(map(lambda a: f"+ {self.add[a.index]}" if a.symbol else f"- {self.remove[a.index]}", self.calclist))
        fullcalc = list(map(lambda a: f"- {self.remove[a]}" if a < len(self.remove) else f"+ {self.add[a - len(self.remove)]}", self.calclist))
        self.ocr.addResult(CalcResult(resulte, fullcalc))
    def generateSum(self):
        shardacc = self.shards
        for b in self.calclist:
            if b < len(self.remove):
                shardacc -= self.remove[b]
            else:
                shardacc += self.add[b - len(self.remove)]
        return shardacc
    def moveListByOne(self):
        for i, a in enumerate(self.calclist, start=0):
            if a < len(self.remove) + len(self.add) - 1:
                self.calclist[i] += 1
                break
            else:
                self.calclist[i] = 0
                if i < len(self.calclist) - 2:
                    continue
    def singleCalc(self, actions):
        if self.gotoscore < self.shards:
            for a in range((len(self.add) + len(self.remove)) ** actions):
                shardacc = self.generateSum()
                # checking display setings and is "shardacc" above 0 
                if (shardacc > 0) and (shardacc <= self.gotoscore):
                    print(self.calclist, shardacc)
                    self.addResulter(shardacc)
                self.moveListByOne()
        else:
            for a in range((len(self.add) + len(self.remove)) ** actions):
                shardacc = self.generateSum()
                # checking display setings and is "shardacc" above 0 
                if (shardacc > self.shards) and (shardacc <= self.gotoscore):
                    print(self.calclist, shardacc)
                    self.addResulter(shardacc)
                self.moveListByOne()
    def calculate(self):
        if self.actionsbelow:
            for a in range(1, self.maxactions+1):
                self.calcfill(a)
                self.singleCalc(a)
        else:
            self.singleCalc(self.maxactionsk)
        self.ocr.uptadeResults(self.gotoscore)
        # print('res::', list(map(lambda a: a.value, self.ocr.resultList)))
        # print('ban::', list(map(lambda a: a.value, self.ocr.banlist)))
        self.ocr.displayConclusion(self.gotoscore, self.allowdq, self.dqv)


# # self, maxactions = 2, actionsbelow = True, shards = 4437, gotoscore = 2137, allowdq = False, dqv = 0

# ma = Main(input('how much shard to use: '), input('allow less shards (y/n): '), input('how much essense do you have: '), input('your goal: '), input('allow dq (daily quests) (y/n): '), input('how much dq you allow: '))
ma = Main()
ma.calculate()

# print(self.ocr.addResult())

print("--- %s seconds ---" % (time.time() - start_time))