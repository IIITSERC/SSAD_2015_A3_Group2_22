import matrix
import time
import random

class Direction():

    SOUTH = 's'
    WEST = 'a'
    EAST = 'd'
    NORTH = 'w'
    JUMP = ' '

class Motion ():

    LEFT = -1
    RIGHT = 1
    REST = 0

class person():

    def __init__(self, startx, starty, symbol, trace, velx = 1, vely = 1):

        self.velx = velx
        self.vely = vely

        self.x = startx
        self.y = starty

        self.symbol = symbol
        self.trace = trace


class gameBadGuy(person):

    def __init__(self, symbol, floor_coordinates, velx = 1, vely = 1, trace = ' '):


        self.starty = floor_coordinates[1][0]-1 #first floor of the map
        self.startx = 7

        self.lim_left = 1
        self.lim_right = floor_coordinates[1][1]-1

        person.__init__(self, self.startx, self.starty, symbol, trace, velx, vely)
        self.x += 5
        self.velx = -1 

    def checkWall(self):

        if self.x + self.velx < self.lim_left or self.x + self.velx > self.lim_right:
            self.velx *= -1

    def move(self, grid, player, autocall = 1):

        if autocall == 1:
            time.sleep(0.02)
        self.checkWall()
        self.checkCollision(player)
        self.x = self.x + self.velx

    def checkCollision(self, player):

        if (self.x == player.x and self.y == player.y) or (self.x + self.velx == player.x and self.y == player.y):
            player.score -= 25
            player.lives -= 1
            player.reset()

    def manageFireball(self, rows, columns, matrix, floor_coordinates, fireball_list):

        for item in fireball_list:
            if item.y == rows-2 and item.x == 1:
                fireball_list.remove(item)
                matrix.grid[rows-2][1] = ' '
        if self.x == self.startx-1 and self.y == self.starty:
            if len(fireball_list)<2:
                new_fireball = fireball('O',floor_coordinates, 1, 1)
                fireball_list.append(new_fireball)
            else:    
                if random.randint(0,1) ==1:
                    new_fireball = fireball('O',floor_coordinates, 1, 1)
                    fireball_list.append(new_fireball)
                    
                
        return fireball_list        

class fireball(gameBadGuy):

    def move(self, columns, matrix, player, ladder, wall, floor, autocall = 1):
        
        if autocall == 1:
	    time.sleep(0.02)
        self.check_wall(columns)
        if matrix.SE_of(self) == matrix.symbol or matrix.SW_of(self) == matrix.symbol:
            self.fall(matrix, player, ladder, wall, floor)
        elif matrix.S_of(self) == ladder.symbol:
            if random.randint(0,1) == 1:
                self.climb_down(matrix, player, ladder, wall, floor)
            else:
                self.checkCollision(player)
                self.x = self.x + self.velx
        else:
            self.checkCollision(player)
            self.x = self.x + self.velx

    def check_wall(self, columns):

        if self.x + self.velx < 1 or self.x + self.velx > columns-2:
            self.velx *= -1

    def fall(self, matrix, player, ladder, wall, floor, autocall = 1):

        offset = self.velx
        while matrix.SE_of(self) == matrix.symbol or matrix.SW_of(self) == matrix.symbol:
            matrix.update_character_in_matrix(self.y, self.x, self.trace)
            matrix.update_ladders_in_matrix(floor.coordinates, ladder.coordinates, ladder.symbol, floor.gap)
            self.y += self.vely
            if matrix.grid[self.y][self.x+offset] != wall:
                self.x += offset
            matrix.update_character_in_matrix(self.y, self.x, self.symbol)
            if autocall == 1:
                time.sleep(0.02)
            matrix.print_matrix(player.score, player.lives)

    def climb_down(self, matrix, player, ladder, wall, floor, autocall = 1):

        while matrix.S_of(self) not in [floor.symbol, wall]:
            self.checkCollision(player)
            matrix.update_character_in_matrix(self.y, self.x, self.trace)
            matrix.update_ladders_in_matrix(floor.coordinates, ladder.coordinates, ladder.symbol, floor.gap)
            self.y += self.vely
            matrix.update_character_in_matrix(self.y, self.x, self.symbol)
            if autocall == 1:
                time.sleep(0.02)
            matrix.print_matrix(player.score, player.lives)

class gameQueen():

    def __init__(self, symbol, floor_coordinates):

        self.x = floor_coordinates[0][0]+3
        self.y = 1

        self.symbol = symbol

class gamePlayer(person):

    def __init__(self, symbol, score = 0, startX = 1, startY = 1, velx = 1, vely = 1, trace = ' ', nlives = 3):

        self.startx = startX
        self.starty = startY 

        self.motion = Motion.REST

        self.lives = nlives
        self.score = score

        person.__init__(self, self.startx, self.starty, symbol, trace, velx, vely)
    
    def winGame(self, princess, matrix):

        if self.x == princess.x and self.y == princess.y:
            self.score += 50
            return 1
        else:
            return 0

    def reset(self):

        self.x = self.startx
        self.y = self.starty

        if self.score < 0:
            self.score = 0

        if self.lives < 0:
            self.lives = 0

    def move(self, direction, limx, limy, matrix, wall, floor, ladder, coin):

       self.collectCoin(matrix, coin)
       self.motion = Motion.REST
       # check floor below
       if matrix.S_of(self) in [floor, ladder] and (matrix.SE_of(self) in [floor, wall, ladder] or matrix.SW_of(self) in [floor, wall, ladder]):

           if direction == Direction.EAST and self.x+1 < limx and matrix.E_of(self) != wall:
               self.x += self.velx
               self.motion = Motion.RIGHT
           elif direction == Direction.WEST and self.x > 0 and matrix.W_of(self) != wall:
               self.x -= self.velx 
               self.motion = Motion.LEFT

    def climb(self, direction, matrix, ladder, floor, coin):

            self.collectCoin(matrix, coin)

            matrix.update_ladders_in_matrix(floor.coordinates, ladder.coordinates, ladder.symbol, floor.gap)

            if direction == Direction.NORTH and matrix.getPosition(self) == ladder.symbol:
                if matrix.N_of(self) == matrix.symbol and matrix.S_of(self) == floor.symbol:
                    return;
                self.y -= self.vely
            elif direction == Direction.SOUTH and matrix.S_of(self) == ladder.symbol:
                self.y += self.vely
            else:
                return

            matrix.update_character_in_matrix(self.y, self.x, self.symbol)

    def jump(self, direction, limx, limy, matrix, ladder, floor, wall, coin, donkey, fireballs, max_height = 2, multiplier = 3):

        self.collectCoin(matrix, coin)

        #direction of jump
        if self.motion == Motion.RIGHT:
            offset = multiplier*self.velx
        elif self.motion == Motion.LEFT:
            offset = -1*multiplier*self.velx
        elif self.motion == Motion.REST:
            offset = 0

        matrix.update_character_in_matrix(self.y, self.x, self.trace)
        #init jump
        if direction == Direction.JUMP and matrix.S_of(self) in [wall, floor.symbol, ladder.symbol]:
            maxjump = self.y-max_height
            initial_height = self.y

            #up
            while self.y > maxjump:
                matrix.update_character_in_matrix(self.y, self.x, self.trace)
                matrix.update_ladders_in_matrix(floor.coordinates, ladder.coordinates, ladder.symbol, floor.gap)
                for fireball in fireballs:
                    matrix.update_character_in_matrix(fireball.y, fireball.x, fireball.trace)
                    fireball.move(limx, matrix, self, ladder, wall, floor, 0)
                    matrix.update_character_in_matrix(fireball.y, fireball.x, fireball.symbol)
                matrix.update_character_in_matrix(donkey.y, donkey.x, donkey.trace)
                donkey.move(matrix.grid, self, 0)
                matrix.update_coins_in_matrix(coin.coordinates, coin.symbol)
                matrix.update_character_in_matrix(donkey.y, donkey.x, donkey.symbol)
                if matrix.N_of(self) != floor.symbol or getPosition(self) != floor.symbol:
                     if matrix.getPosition(self) == ladder.symbol and self.motion != Motion.REST:
                         break
                     self.y -= self.vely
                else:
                     break
                if self.x + offset not in range(1,limx-2):
                     if self.motion == Motion.RIGHT:
                         self.x = limx-2
                         offset = 0
                     elif self.motion == Motion.LEFT:
                         self.x = 1
                         offset = 0
                else:
                     self.x += offset
                matrix.update_character_in_matrix(self.y, self.x, self.symbol)
                time.sleep(0.05)
                matrix.print_matrix(self.score, self.lives)

            #down    
            while matrix.S_of(self) in [matrix.symbol, 'o', coin.symbol]:
                self.collectCoin(matrix, coin)
                matrix.update_character_in_matrix(self.y, self.x, self.trace)
                matrix.update_ladders_in_matrix(floor.coordinates, ladder.coordinates, ladder.symbol, floor.gap)
                for fireball in fireballs:
                    matrix.update_character_in_matrix(fireball.y, fireball.x, fireball.trace)
                    fireball.move(limx, matrix, self, ladder, wall, floor, 0)
                    matrix.update_character_in_matrix(fireball.y, fireball.x, fireball.symbol)
                matrix.update_character_in_matrix(donkey.y, donkey.x, donkey.trace)
                donkey.move(matrix.grid, self, 0)
                matrix.update_coins_in_matrix(coin.coordinates, coin.symbol)
                matrix.update_character_in_matrix(donkey.y, donkey.x, donkey.symbol)
                if matrix.getPosition(self) == ladder.symbol and self.motion != Motion.REST:
                    break
                self.y += self.vely
                if self.x + offset not in range(1,limx-1):
                    if self.motion == Motion.RIGHT:
                        self.x = limx-2
                        offest = 0
                    elif self.motion == Motion.LEFT: 
                        self.x = 1
                        offset = 0
                else:
                    self.x += offset
                matrix.update_character_in_matrix(self.y, self.x, self.symbol)
                time.sleep(0.05)
                matrix.print_matrix(self.score, self.lives)

    def fall(self, limx, direction, matrix, ladder, floor, wall, coin, donkey, fireballs):

        self.collectCoin(matrix, coin)

        #direction of fall
        if direction == Direction.EAST:
            offset = self.velx
        elif direction == Direction.WEST:
            offset = -1*self.velx
        else: 
            offset = 0
        if ((direction == Direction.EAST and matrix.SE_of(self) == matrix.symbol) or (direction == Direction.WEST and matrix.SW_of(self) == matrix.symbol) or matrix.getPosition(self) == matrix.symbol):
            while matrix.grid[self.y+self.vely][self.x+offset] in [matrix.symbol, 'o', coin.symbol]:
                self.collectCoin(matrix, coin)
                matrix.update_character_in_matrix(self.y, self.x, self.trace)
                matrix.update_ladders_in_matrix(floor.coordinates, ladder.coordinates, ladder.symbol, floor.gap)
                for fireball in fireballs:
                    matrix.update_character_in_matrix(fireball.y, fireball.x, fireball.trace)
                    fireball.move(limx, matrix, self, ladder, wall, floor, 0)
                    matrix.update_character_in_matrix(fireball.y, fireball.x, fireball.symbol)
                matrix.update_character_in_matrix(donkey.y, donkey.x, donkey.trace)
                donkey.move(matrix.grid, self, 0)
                matrix.update_coins_in_matrix(coin.coordinates, coin.symbol)
                matrix.update_character_in_matrix(donkey.y, donkey.x, donkey.symbol)
                self.y += self.vely
                if matrix.grid[self.y][self.x+offset] != wall:
                    self.x += offset
                matrix.update_character_in_matrix(self.y, self.x, self.symbol) 
                #                time.sleep(0.05)
                matrix.print_matrix(self.score, self.lives)

    def collectCoin(self, matrix, coin):

        if [self.y, self.x] in coin.coordinates:
            coin.coordinates.remove([self.y, self.x])
            self.score += 5

class gameWall():

    def __init__(self, symbol, rows, columns, coordinates = []):

        self.symbol = symbol
        self.coordinates = coordinates

        for i in xrange(rows):
            self.coordinates.append([i,0])
            self.coordinates.append([i,columns-1])

        for i in xrange(columns):
            self.coordinates.append([0,i])
            self.coordinates.append([rows-1,i])


class gameFloor():

    def __init__(self, symbol, rows, columns, startFloor = 5, gap = 4, offset = 5): 

        self.symbol = symbol
        self.coordinates = []
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

class gameLadder():

    def __init__(self, symbol, floor_coordinates):

        self.symbol = symbol
        self.coordinates = []

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

class gameCoin():

    def __init__(self, symbol, floor_coordinates, columns, coin_per_floor = 5):

        self.symbol = symbol
        self.coordinates = []

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

