import time
import sys
import matrix
import living
import nonliving
import keyboard
from living import *
from nonliving import *
from select import select
import sys, termios, atexit
import random

atexit.register(keyboard.set_normal_term)
keyboard.set_curses_term()

rows, columns = 26, 111
score = 0
next_level = True

game_matrix = matrix.gameMatrix(rows, columns)

def main():

    global rows
    global columns
    global score
    global next_level

    game_player = gamePlayer('P', score, 7, rows-2)
    game_wall = gameWall('X', rows, columns)
    game_floor = gameFloor('X', rows, columns)
    game_ladder = gameLadder('H', game_floor.coordinates)
    game_coin = gameCoin('c', game_floor.coordinates, columns)
    game_donkey = gameBadGuy('D', game_floor.coordinates)
    game_fireball_list = []
    game_princess = gameQueen('Q', game_floor.coordinates)

    game_matrix.update_walls_in_matrix(game_wall.coordinates, game_wall.symbol)
    game_matrix.update_floors_in_matrix(game_floor.coordinates, game_wall.symbol, columns)
    game_matrix.update_ladders_in_matrix(game_floor.coordinates, game_ladder.coordinates, game_ladder.symbol, game_floor.gap)
    game_matrix.update_coins_in_matrix(game_coin.coordinates, game_coin.symbol)
    game_matrix.update_character_in_matrix(game_player.y, game_player.x, game_player.symbol)
    game_matrix.update_character_in_matrix(game_donkey.y, game_donkey.x, game_donkey.symbol)
    game_matrix.update_character_in_matrix(game_princess.y, game_princess.x, game_princess.symbol)

    while True:
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        game_matrix.update_character_in_matrix(game_donkey.y, game_donkey.x, game_donkey.trace)
        game_fireball_list = game_donkey.manageFireball(rows, columns, game_matrix, game_floor.coordinates, game_fireball_list)
        for fireball in game_fireball_list:
            game_matrix.update_character_in_matrix(fireball.y, fireball.x, fireball.trace)
            fireball.move(columns, game_matrix, game_player, game_ladder, game_wall.symbol, game_floor)
            game_matrix.update_character_in_matrix(fireball.y, fireball.x, fireball.symbol)
        game_donkey.move(game_matrix.grid, game_player)
        game_matrix.update_ladders_in_matrix(game_floor.coordinates, game_ladder.coordinates, game_ladder.symbol, game_floor.gap)
        game_matrix.update_coins_in_matrix(game_coin.coordinates, game_coin.symbol)
        game_matrix.update_character_in_matrix(game_donkey.y, game_donkey.x, game_donkey.symbol)
        game_matrix.update_character_in_matrix(game_player.y, game_player.x, game_player.symbol)
        
        game_matrix.print_matrix(game_player.score, game_player.lives)

        direction = None    

        start = time.time()
        if keyboard.kbhit():
            
            direction = keyboard.getch()
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            time.sleep(0.01)
        end = time.time()
        if(end - start > 0.3):
            game_player.motion = Motion.REST

        if direction == 'q' or game_player.lives == 0:
            next_level = False
            return
        elif game_player.winGame(game_princess, game_matrix) == 1: 
            score = game_player.score
            game_matrix.print_matrix(game_player.score, game_player.lives)
	    game_matrix.reset(columns, rows)
	    game_matrix.level += 1
	    time.sleep(3)
            del game_player
            del game_wall
            del game_floor
            del game_ladder
            del game_coin
            del game_donkey
            game_fireball_list = []
            del game_princess
            return
        elif direction not in (Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST, Direction.JUMP):
            continue
        else:
            game_matrix.update_character_in_matrix(game_player.y, game_player.x, game_player.trace)
            game_player.climb(direction, game_matrix, game_ladder, game_floor, game_coin)
            game_player.jump(direction, columns, rows, game_matrix, game_ladder, game_floor, game_wall.symbol, game_coin, game_donkey, game_fireball_list)
            game_player.fall(columns, direction, game_matrix, game_ladder, game_floor, game_wall.symbol, game_coin, game_donkey, game_fireball_list)
            game_matrix.update_character_in_matrix(game_player.y, game_player.x, game_player.trace)
            game_player.move(direction, columns, rows, game_matrix, game_wall.symbol, game_floor.symbol, game_ladder.symbol, game_coin)
            game_matrix.update_ladders_in_matrix(game_floor.coordinates, game_ladder.coordinates, game_ladder.symbol, game_floor.gap)
            game_matrix.update_coins_in_matrix(game_coin.coordinates, game_coin.symbol)
            game_matrix.update_character_in_matrix(game_player.y, game_player.x, game_player.symbol)

if __name__ == '__main__':
    while True:
        if next_level == True:
            main()
        else:
            break
