print('ayy')
def plus(a, b):
    return a + b
def minus(a, b):
    return a - b
class calcpart:
    def __init__(self, symbol, minusindex, plusindex):
        self.symbol = symbol
        self.minusindex = minusindex
        self.plusindex = plusindex
    def so(self):
        if self.symbol == False:
            return 0
        else:
            return 1
    def __repr__(self):
        return f"(-{self.minusindex} , {self.so()}, +{self.plusindex} )"

# 450 +90 -270
# 1350 +270 -810
# 3150 +630 - 1890
# 4800 +960 -2880
# 6300 +1260 -3780
# 7800 +1560 -4680

class Main:
    def __init__(self, maxactions = 2, actionsbelow = True, shards = 4437, gotoscore = 2137, allowmoe = True, moev = 250):
    # def __init__(self, actionsbelow = True, add = [0, 90, 270, 630, 960, 1260, 1560], remove = [0, 450, 1350, 3150, 4800, 6300, 7800, 270, 810, 1890, 2880, 3780, 4680], maxactions = 7, shards = 4437, gotoscore = 2137, moev = 100):
        if allowmoe == 'y':
            self.allowmoe = True
        elif allowmoe == 'n':
            self.allowmoe = False
        else:
            raise ValueError('got sth else than "y" or "n" in moe')
        if actionsbelow == 'y':
            self.actionsbelow = True
        elif actionsbelow == 'n':
            self.actionsbelow = False
        else:
            raise ValueError('got sth else than "y" or "n" in actionsbelow')
        if self.actionsbelow:
            self.add = [0, 90, 270, 630, 960, 1260, 1560]
            self.remove = [0, 450, 1350, 3150, 4800, 6300, 7800, 270, 810, 1890, 2880, 3780, 4680]
        else:
            self.add = [90, 270, 630, 960, 1260, 1560]
            self.remove = [450, 1350, 3150, 4800, 6300, 7800, 270, 810, 1890, 2880, 3780, 4680]
        self.maxactions = int(maxactions)
        self.shards = int(shards)
        self.gotoscore = int(gotoscore)
        self.moev = int(moev)
        self.calclist = []
        self.calcfill(self.maxactions)
        print('ab: ', self.actionsbelow, 'am: ', self.allowmoe)
    def calcfill(self, howmuch):
        a = 0
        while a < howmuch:
            self.calclist.append(calcpart(False, 0, 0))
            a = a + 1
    def ischecked(self):
        for a in self.calclist:
            if a.symbol:
                if a.index != len(self.add):
                    return False
            else:
                return False
        return True
    def movelistbyone(self):
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
    def calculate(self):
        multi0count = 0
        while True:
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
            prr = False
            if self.actionsbelow:
                noaction = 0
                for a in self.calclist:
                    if (a.minusindex + a.plusindex) == 0:
                        noaction = noaction + 1
                if noaction != self.maxactions:
                    if self.gotoscore < self.shards:
                        if self.allowmoe:
                            if (shardacc >= (self.gotoscore - self.moev)) and (shardacc <= self.gotoscore):
                                prr = not prr
                        elif (shardacc > 0) and (shardacc <= self.gotoscore):
                            prr = not prr
                    else:
                        if self.allowmoe:
                            if (shardacc >= (self.gotoscore - self.moev)) and (shardacc <= self.gotoscore):
                                prr = not prr
                        elif (shardacc > self.shards) and (shardacc <= self.gotoscore):
                            prr = not prr
            else: 
                if self.gotoscore < self.shards:
                    if self.allowmoe:
                        if (shardacc >= (self.gotoscore - self.moev)) and (shardacc <= self.gotoscore):
                            prr = not prr
                    elif (shardacc > 0) and (shardacc <= self.gotoscore):
                        prr = not prr
                else:
                    if self.allowmoe:
                        if (shardacc >= (self.gotoscore - self.moev)) and (shardacc <= self.gotoscore):
                            prr = not prr
                    elif (shardacc > self.shards) and (shardacc <= self.gotoscore):
                        prr = not prr
            if prr:    
                print(self.calclist, shardacc)
            negstackacc = 0
            for stack in self.calclist:
                if (stack.minusindex or stack.plusindex or stack.symbol) == False:
                    negstackacc = negstackacc + 1
            if negstackacc == self.maxactions:
                if multi0count < 1:
                    multi0count = multi0count + 1
                    print(multi0count)
                else:
                    break
            self.movelistbyone()
# self, maxactions = 2, actionsbelow = True, shards = 4437, gotoscore = 2137, allowmoe = True, moev = 250

ma = Main(input('how much shard to use: '), input('allow less shards (y/n): '), input('how much essense do you have: '), input('your goal: '), input('allow moe (margin of error) (y/n): '), input('how much: '))
ma.calculate()