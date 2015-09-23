import os
import random
import time

class gameMatrix():

    def __init__(self, rows, columns, default_character = ' '):

        self.rows = rows 
        self.columns = columns
        self.symbol = default_character
        self.level = 1

        self.grid = [ [default_character] * columns for _ in xrange(rows) ]

    def reset(self, columns, rows):

	for i in xrange(rows):
	    for j in xrange(columns):
		self.grid[i][j] = self.symbol
    
    def getPosition(self, person):

        return self.grid[person.y][person.x]

    def N_of(self, person):

        return self.grid[person.y-1][person.x]

    def S_of(self, person):

        return self.grid[person.y+1][person.x]

    def E_of(self, person):

        return self.grid[person.y][person.x+1]

    def W_of(self, person):

        return self.grid[person.y][person.x-1]

    def NW_of(self, person):

        return self.grid[person.y-1][person.x-1]

    def NE_of(self, person):

        return self.grid[person.y-1][person.x+1]

    def SE_of(self, person):

        return self.grid[person.y+1][person.x+1]

    def SW_of(self, person):

        return self.grid[person.y+1][person.x-1]

    def print_matrix(self, score, lives):
        
        #os.system('clear')
        os.system("printf '\033c'")

        print "\n"
	print "\t\t\t\t\t\t\t______Donkey Kong - Save the Princess!______\n"
        print "\t\t\t\t\t\t\t _________________________________________"
        print "\t\t\t\t\t\t\t | score: %d\t level: %d\tlives: %d |" %(score, self.level, lives)
	print "\t\t\t\t\t\t\t -----------------------------------------"
	        
	s = ''
        for row in self.grid:
            s += '\t\t\t'
	    for c in row:
		if c == ' ':
		    s = s + c    			
		elif c == 'X':
		    s = s + '\033[34m' + c + '\033[0;0m'
		elif c == 'H':
		    s = s + '\033[32m' + c + '\033[0;0m'
		elif c == 'c':
		    s = s + '\033[33m' + c + '\033[0;0m'
		elif c == 'O':
		    s = s + '\033[31m' + c + '\033[0;0m'
		elif c == 'P':
		    s = s + '\033[37m' + c + '\033[0;0m'
		elif c == 'D':
		    s = s + '\033[35m' + c + '\033[0;0m'
		elif c == 'Q':
		    s = s + '\033[36m' + c + '\033[0;0m'
	    s += '\n'

        print s 
	
	print "\t\t\t\t\t\t                             Game-Controls                            \n"
	print "\t\t\t\t\t\t______________________________________________________________________"
        print "\t\t\t\t\t\t| W : up | A : left | S : down | D : right | Space : jump | Q : quit |"
	print "\t\t\t\t\t\t----------------------------------------------------------------------"

	time.sleep(0.01)

 
    def update_character_in_matrix(self, row_number, column_number, new_character):

        if 0 <= row_number and row_number < self.rows and 0 <= column_number and column_number < self.columns:
            self.grid[row_number][column_number] = new_character
        else:
            raise IndexError(" Index error. Index is out of bounds ")    
    
    def update_walls_in_matrix(self, coordinates, wall_character):

        for pair in coordinates:
            self.grid[pair[0]][pair[1]] = wall_character

    def update_floors_in_matrix(self, coordinates, floor_character, columns):

        # princess cage
        pair = coordinates[0]
        for i in range(pair[0], pair[1]+1, 1):
            self.grid[2][i] = floor_character
        self.grid[1][pair[0]] = floor_character
        self.grid[1][pair[1]] = floor_character
        

        for i in range(1, len(coordinates)):
            pair = coordinates[i]
            if i % 2 == 1:
                for j in range(0, pair[1], 1):
                    self.grid[pair[0]][j] = floor_character
            else:
                for j in range(pair[1], columns-1, 1):
                    self.grid[pair[0]][j] = floor_character

    def update_ladders_in_matrix(self, floor_coordinates, ladder_coordinates, ladder_character, floor_gap):
        
        # princess cage ladder (also princess initialised in here) ********************************************************************
        pair = floor_coordinates[0]
        for j in range(2,floor_coordinates[1][0]):
            self.grid[j][pair[1]-2] = ladder_character

        for i in range(1,len(ladder_coordinates)):
            for p in xrange(len(ladder_coordinates[i])):
                if len(ladder_coordinates[i]) == 1:
                    for j in range(floor_coordinates[i][0],floor_coordinates[i+1][0]):
                        self.grid[j][ladder_coordinates[i][0]] = ladder_character
                elif len(ladder_coordinates[i]) == 2:
                    broken_ladder = 1
                    if i % 2 == 0: # to decide which of the 2 ladders is broken
                        broken_ladder = 0
                    fine_ladder = 1 - broken_ladder
                    for j in range(floor_coordinates[i][0],floor_coordinates[i+1][0]):
                        self.grid[j][ladder_coordinates[i][fine_ladder]] = ladder_character
                    for j in range(floor_coordinates[i][0],floor_coordinates[i+1][0]):
                        if j != floor_coordinates[i+1][0]-2:
                            self.grid[j][ladder_coordinates[i][broken_ladder]] = ladder_character

    def update_coins_in_matrix(self, coin_coordinates, coin_character):

        for pair in coin_coordinates:
            self.grid[pair[0]][pair[1]] = coin_character
