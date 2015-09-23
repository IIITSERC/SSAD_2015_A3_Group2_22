import matrix
import time
import random

class nonliving():

    def __init__(self, symbol):

	self.symbol = symbol
	self.coordinates = []

class gameWall(nonliving):

    def __init__(self, symbol, rows, columns):

        nonliving.__init__(self, symbol)

        for i in xrange(rows):
            self.coordinates.append([i,0])
            self.coordinates.append([i,columns-1])

        for i in xrange(columns):
            self.coordinates.append([0,i])
            self.coordinates.append([rows-1,i])


class gameFloor(nonliving):

    def __init__(self, symbol, rows, columns, startFloor = 5, gap = 4, offset = 5): 

        nonliving.__init__(self, symbol)        

        self.gap = gap
        self.startFloor = startFloor
        self.offset = offset # offset is half the intersection between 2 floors

        mid = (rows + columns) / 2

        x = random.randint(20, columns/2 - 30) # for princess cage

        self.coordinates.append([x,x+11])

        # random floor
        for i in range(startFloor, rows, gap):
            if ((i - startFloor) / gap) % 2 == 0:
                self.coordinates.append([i,random.randint(mid + offset,columns - offset)])
            else:
                self.coordinates.append([i,random.randint(offset,mid - offset)])

class gameLadder(nonliving):

    def __init__(self, symbol, floor_coordinates):

        nonliving.__init__(self, symbol)

        # build ladder between intersection between two levels
        for i in range(0,len(floor_coordinates)-1):

            left = floor_coordinates[i][1]
            right = floor_coordinates[i+1][1]
            if left > right: 
                left, right = right, left

            nladders = random.randint(1,2) # number of ladders for a level 1 or 2

            tp = []

            for i in xrange(nladders):
                tp.append(random.randint(left+2,right-2))

            self.coordinates.append(tp)                

class gameCoin(nonliving):

    def __init__(self, symbol, floor_coordinates, columns, coin_per_floor = 5):

        nonliving.__init__(self, symbol)

        self.ncoins = coin_per_floor # number of coins per floor

        for i in range(1,len(floor_coordinates)):
            for j in xrange(5):

                tp = []
                pair = floor_coordinates[i]

                if i % 2 == 1:
                    tp.append(pair[0]-1) # -1 for top of floor
                    tp.append(random.randint(1, pair[1]-1))
                else:
                    tp.append(pair[0]-1) 
                    tp.append(random.randint(pair[1], columns-2))

                self.coordinates.append(tp)    

