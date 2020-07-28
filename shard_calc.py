def plus(a, b):
    return a + b
def minus(a, b):
    return a - b
class Calcpart:
    def __init__(self, symbol, minusindex, plusindex):
        self.symbol = symbol
        self.minusindex = minusindex
        self.plusindex = plusindex
    def symbolDisplay(self):
        if self.symbol:
            return 1
        else:
            return 0
    def __repr__(self):
        return f"(-{self.minusindex} , {self.symbolDisplay()}, +{self.plusindex} )"

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
                    anacc = anacc + 1
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
    def displayConclusion(self, goal):
        optimalgoallist = []
        for a in self.resultList:
            if a.value == goal:
                lencheck = len(a.wayToGet[0])
                for b in a.wayToGet:
                    if len(b) == lencheck:
                        optimalgoallist.append(b)
        optimalgoallist = list(map(lambda n: ' '.join(n), optimalgoallist))
        optimalgoallist = ',\n'.join(optimalgoallist)
        print(f'optimal goal: \n{optimalgoallist}')
        
class CalcResult:
    def __init__(self, value, wayToGet):
        self.value = value
        self.wayToGet = [wayToGet]
    def __repr__(self):
        return f"\n{self.value} : {self.wayToGet}\n"

# 450 +90 -270
# 1350 +270 -810
# 3150 +630 - 1890
# 4800 +960 -2880
# 6300 +1260 -3780
# 7800 +1560 -4680

class Main:
    def __init__(self, maxactions = 3, actionsbelow = 'y', shards = 450, gotoscore = 630, allowdq = 'n', dqv = 0):
        if allowdq == 'y':
            self.allowdq = True
        elif allowdq == 'n':
            self.allowdq = False
        else:
            raise ValueError('got sth else than "y" or "n" in moe')
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
        self.calclist = []
        a = 0
        while a < howmuch:
            self.calclist.append(Calcpart(False, 0, 0))
            a = a + 1
    def addResulter(self, resulte):
        fullcalc = []
        for a in self.calclist:
            if a.symbol:
                fullcalc.append(f"+ {self.add[a.plusindex]}")
            else:
                fullcalc.append(f"- {self.remove[a.minusindex]}")
        self.ocr.addResult(CalcResult(resulte, fullcalc))
        # self.ocr.addResult(resulte)
    def generateSum(self):
        shardacc = 0
        for i, b in enumerate(self.calclist, start=0):
            if i > 0:
                if b.symbol:
                    shardacc = plus(shardacc, self.add[b.plusindex])
                else:
                    shardacc = minus(shardacc, self.remove[b.minusindex])
            else:
                if b.symbol:
                    shardacc = plus(self.shards, self.add[b.plusindex])
                else:
                    shardacc = minus(self.shards, self.remove[b.minusindex])
        return shardacc
    def moveListByOne(self):
        for i, a in enumerate(self.calclist, start=0):
            if a.symbol == False:
                if a.minusindex < len(self.remove) - 1:
                    self.calclist[i].minusindex = self.calclist[i].minusindex + 1
                    break
                else:
                    self.calclist[i].minusindex = 0
                    self.calclist[i].symbol = not self.calclist[i].symbol
                    break
            else:
                if a.plusindex < len(self.add) - 1:
                    self.calclist[i].plusindex = self.calclist[i].plusindex + 1
                    break
                else:
                    self.calclist[i].plusindex = 0
                    self.calclist[i].symbol = not self.calclist[i].symbol
                    if i < len(self.calclist) - 2:
                        continue
    def singleCalc(self, actions):
        multi0count = 0
        while True:
            shardacc = self.generateSum()
            prr = False
            # checking display setings and is "shardacc" above 0 
            if self.gotoscore < self.shards:
                if self.allowdq:
                    if (shardacc >= (self.gotoscore - self.dqv)) and (shardacc <= self.gotoscore):
                        prr = not prr
                elif (shardacc > 0) and (shardacc <= self.gotoscore):
                    prr = not prr
            else:
                if self.allowdq:
                    if (shardacc >= (self.gotoscore - self.dqv)) and (shardacc <= self.gotoscore):
                        prr = not prr
                elif (shardacc > self.shards) and (shardacc <= self.gotoscore):
                    prr = not prr
            if prr:    
                print(self.calclist, shardacc)
                self.addResulter(shardacc)
            # checking is all possibilities tested
            negstackacc = 0
            for stack in self.calclist:
                if (stack.minusindex or stack.plusindex or stack.symbol) == False:
                    negstackacc = negstackacc + 1
            if negstackacc == actions:
                if multi0count < 1:
                    multi0count = multi0count + 1
                    print(multi0count)
                else:
                    break
            self.moveListByOne()
    def calculate(self):
        if self.actionsbelow:
            # actAction = self.maxactions
            # while actAction > 0:
            #     self.calcfill(actAction)
            #     self.singleCalc(actAction)
            #     actAction = actAction - 1
            for a in range(1, self.maxactions+1):
                self.calcfill(a)
                self.singleCalc(a)
        else:
            self.singleCalc(self.maxactionsk)    
        self.ocr.uptadeResults(self.gotoscore)
        print('res::', self.ocr.resultList)
        print('ban::', self.ocr.banlist)
        self.ocr.displayConclusion(self.gotoscore)

# # self, maxactions = 2, actionsbelow = True, shards = 4437, gotoscore = 2137, allowdq = False, dqv = 0

# ma = Main(input('how much shard to use: '), input('allow less shards (y/n): '), input('how much essense do you have: '), input('your goal: '), input('allow dq (daily quests) (y/n): '), input('how much dq you allow: '))
ma = Main()
ma.calculate()

# print(self.ocr.addResult())