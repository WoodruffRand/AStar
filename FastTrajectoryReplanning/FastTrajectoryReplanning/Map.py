class Map(object):
    """Class used to encapsulate and update map data inorder to maintain for of war"""
    
    def __init__(self, fileName):
        mapSource = open(fileName, 'r')
        self.m = 0
        self.n = 0
        self.tM = 0
        self.tN = 0
        self.visMap =[]
        self.hiddenMap = []
        for y, str in enumerate(mapSource.read().split('\n')):
            x = str.find('A')
            if x>-1:
                self.m=x
                self.n=y
            x = str.find('T')
            if x>-1:
                self.tM=x
                self.tN=y
            self.hiddenMap.append(( list(str) ))
        
    
        self.initVis()
        mapSource.close()

    def initVis(self):
        for i in range( len(self.hiddenMap)):
            self.visMap.append(list())
            for j in range( len(self.hiddenMap)):
                self.visMap[i].append("?")
        self.updateVis()
        
    def updateVis(self):
        self.visMap[self.n][self.m] = self.hiddenMap[self.n][self.m]
        if self.m-1 > -1:
            self.visMap[self.n][self.m-1] = self.hiddenMap[self.n][self.m-1]
        if self.n-1 > -1:
            self.visMap[self.n-1][self.m] = self.hiddenMap[self.n-1][self.m]
        if self.m+1 < len(self.hiddenMap):
            self.visMap[self.n][self.m+1] = self.hiddenMap[self.n][self.m+1]
        if self.n+1 < len(self.hiddenMap):
            self.visMap[self.n+1][self.m] = self.hiddenMap[self.n+1][self.m]


    def getMap(self):
        return self.visMap

    def isDone(self):
        return self.m == self.tM and self.n == self.tN
    
    def getT(self):
        return [self.tN, self.tM]

    def move(self,n,m):
        if m < -1 or 1< m:
            raise ValueError("Invlid move function call: improper value of m")
        if n < -1 or 1< n:
            raise ValueError("Invlid move function call: improper value of n")

        if (self.m + m <0 or len(self.visMap)-1< self.m + m) and (self.n +n <0 or len(self.visMap)-1 < self.n+n ):#both invalid
            return False
        elif self.m + m <0 or len(self.visMap)-1< self.m + m: #m invliad
            return False
        elif self.n +n <0 or len(self.visMap)-1 < self.n+n:#n invalid
            return False
        else:# both ok
            if self.hiddenMap[self.n+n][self.m+m] == "B":
                return False # way is blocked! invalid move
            self.visMap[self.n][self.m] = ' '
            self.hiddenMap[self.n][self.m] = ' '
            self.m += m
            self.n += n
            self.visMap[self.n][self.m] = 'A'
            self.hiddenMap[self.n][self.m] = 'A'
        self.updateVis()
        return True

    def validCell(self, c):
        if c[0]<0 or c[0] >=len(self.visMap):
            return False
        if c[1]<0 or c[1] >=len(self.visMap):
            return False
        if self.visMap[c[0]][c[1]] == "B":
            return False
        return True

    def isTarget(self, c):    
         try:
             return self.hiddenMap[c[0]][c[1]] =='T'
         except:
             print("moooo")


    def genTopBoarder(self):
        tb = u'\u250f'
        for i in range(2*len(self.visMap)+6):
            tb+=u'\u2501' 
        tb+= u'\u2513'
        return tb

    def genBottomBoarder(self):
        tb = u'\u2517'
        for i in range(2*len(self.visMap)+6):
            tb+= u'\u2501' 
        tb+= u'\u251B' 
        return tb

    def display(self):
        
        print(self.genTopBoarder())
        for vRow, hRow  in zip(self.visMap, self.hiddenMap):
            line =u'\u2503'
            line += "".join(vRow)
            line +="  " +u'\u2503'+u'\u2503' +"  "
            line += "".join(hRow)
            line += u'\u2503'
            print(line)
        print(self.genBottomBoarder())