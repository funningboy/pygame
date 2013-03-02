#-* coding:UTF-8 -*
#!/usr/bin/env python

""" origin file is from """

import copy
import pygame
import random

ALL_BLOCKS = [
                [
                    [0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0],
                    [0, 1, 0, 0, 0],
                    [0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ],
                [
                    [0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ]
             ]

def get_block():
    return random.choice(ALL_BLOCKS)

def get_line_block():
    return ALL_BLOCKS[0]

def rorate_block(block):
    '''
        rotate 90 degree
    '''
    new_block = [[0 for col in range(5)] for row in range(5)]
    for x in range(5):
        for y in range(4, -1, -1):
            new_block[y][x] = block[x][4 - y]
    return new_block
    #return zip(*block) ???


def print_block(block):
    for line in block:
        print '%s \n' % line


def init_map(max_x, max_y, wall_widith, wall_height):
    '''
        initial map and wall setup
    '''
    maps = [[0 for col in range(max_x)]for cell in range(max_y)]
    for y in range(max_y):
        for x in range(max_x):
            if x < wall_widith or x > max_x - wall_widith - 1 or y > max_y - wall_height:
                    maps[y][x] = 1
    return maps



SCREEN_SIZE = WIDTH, HEIGHT = [480, 660]
BACKGROUND_COLOR = (0, 0, 0)
BLOCK_COLOR = (0, 0, 255)
WALL_COLOR = (0, 0, 255)

WALL_WIDTH = 3
WALL_HEIGHT = 4
#map start map point
MAP_BEGIN_POINT = [0, 0]
MAX_X, MAX_Y = 16, 22
RECT_SIZE = [WIDTH/MAX_X, HEIGHT/MAX_Y]
CENTER_X = int(MAX_X / 2) - 3
MAP_DATA = init_map(MAX_X, MAX_Y, WALL_WIDTH, WALL_HEIGHT)
BLOCK_START_POINT = [CENTER_X, -1]
# set update rate
FPS = 40
SPEED = 1
FALL_PER_SECONDS = 1


def draw(block_data, start_point, map_data, screen):
    '''
        draw pygame
    '''
    _map_data = copy.deepcopy(map_data)
    _map_start_point = MAP_BEGIN_POINT[:]
    update_map(block_data, start_point, _map_data)
    #print_block(_map_data)
    begin_x = _map_start_point[0]
    for line in _map_data:
        for block in line:
            #print 'draw at %s,%s' % (_start_point[0],_start_point[1])
            rect = pygame.Rect(_map_start_point, RECT_SIZE)
            if block == 0: # filled all if it's background type
		    pygame.draw.rect(screen, BLOCK_COLOR, rect)
            if block == 1:
                pygame.draw.rect(screen, WALL_COLOR, rect, 1)
            _map_start_point[0] += RECT_SIZE[0] #update X
        _map_start_point[1] += RECT_SIZE[1] # update Y
        _map_start_point[0] = begin_x


def update_map(block_data, start_point, map_data):
    '''
	update map
    '''
    _start_point_x = start_point[0]
    _start_point_y = start_point[1]
    for y in range(5):
        for x in range(5):
            # check it's out of range in Wall?
            #print '_start_point_x is %s' % _start_point_x
            #print 'map_data[%s][%s] % s' % (_start_point_y+y,_start_point_x+x,map_data[_start_point_y+y][_start_point_x+x])
            if _start_point_x + x <= WALL_WIDTH - 1 or _start_point_x + x >= MAX_X - WALL_WIDTH:
                continue
            if map_data[_start_point_y + y][_start_point_x + x] != 1:
                map_data[_start_point_y + y][_start_point_x + x] = block_data[y][x]



def can_move(block_data, start_point, map_data):
   '''
   check it can move or not in wall boundary case
   '''
   _start_point_x = start_point[0]
   _start_point_y = start_point[1]
   for y in range(5):
       for x in range(5):
           #print 'map_data[%s][%s] is: %s' % (_start_point_y + y, _start_point_x + x, map_data[_start_point_y + y][_start_point_x + x])
           if block_data[y][x] and map_data[_start_point_y + y][_start_point_x + x]:
                return False
   return True


def get_clear_lines(map_data):
    '''
    check it's clear or not, if it can clear, then return it's Y position
    '''
    full_line_y_list = []
    for y in range(-WALL_HEIGHT, -MAX_Y + 1, -1):
        if len([x for x in map_data[y] if x == 1]) == MAX_X:
            full_line_y_list.append(y)
            for y2 in range(1, 4):
                if len([x for x in map_data[y - y2] if x == 1]) == MAX_X:
                    full_line_y_list.append(y - y2)
            break;
    return full_line_y_list


def clear_lines(map_data):
    '''
    clear lines when the Xs are all filled in 1
    '''
    full_line_y_list = get_clear_lines(map_data)
    while full_line_y_list:
        for full_line_y in full_line_y_list:
            print 'full_line_y: %s' % full_line_y
            for y in range(full_line_y, -MAX_Y + 1, -1):
                for x in range(WALL_WIDTH, MAX_X - WALL_WIDTH):
                    #print 'map_data[%s][%s] =  map_data[%s][%s]' % (y,x,y-1,x)
                    map_data[y][x] = map_data[y - 1][x]
        #print_block(map_data)
        full_line_y_list = get_clear_lines(map_data)
        print 'full_line_y_list is %s' % full_line_y_list


def reach_bottom(block_data,block_left_top,map_data):
    '''
    move to bottom
    '''
    _block_left_top_x = block_left_top[0]
    _block_left_top_y = block_left_top[1]
    max_move_y = 0
    for y in range(1,MAX_Y-WALL_HEIGHT+1):
        if can_move(block_data, [_block_left_top_x, _block_left_top_y + y], map_data):
            max_move_y += 1
        else:
            break
    if max_move_y:
        block_left_top[1] += max_move_y
        update_map(block_data, block_left_top, map_data)
        clear_lines(map_data)

    print 'max_move_y is %s' % max_move_y
    return max_move_y





def main():
    pygame.init()

    clock = pygame.time.Clock()

    time_passed = 0

    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    screen.fill(BACKGROUND_COLOR)
    map_data = copy.deepcopy(MAP_DATA)
    block_data = get_block()
    block_left_top = BLOCK_START_POINT[:]
    draw(block_data, block_left_top, map_data, screen)
    #print 'can_move: %s' % can_move(block_data,block_left_top,map_data)
    pygame.display.flip()
    running = True
    try:
        while running:

            time_passed_seconds = clock.tick(FPS) / 1000.0

            time_passed += time_passed_seconds
            #print 'moved: %s' % moved

            if int(round(time_passed))/FALL_PER_SECONDS == 1:
                _block_left_top_x = block_left_top[0]
                _block_left_top_y = block_left_top[1]
                _block_left_top_y += SPEED
                if can_move(block_data,[_block_left_top_x,_block_left_top_y],map_data):
                    block_left_top[1] = _block_left_top_y
                else:
                    update_map(block_data, block_left_top, map_data)
                    clear_lines(map_data)
                    block_data = get_block()
                    block_left_top = BLOCK_START_POINT[:]
                time_passed = 0


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    _block_left_top_x = block_left_top[0]
                    _block_left_top_y = block_left_top[1]
                    if event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_DOWN:
                        if not reach_bottom(block_data,block_left_top,map_data):
                            print 'game over'
                            pygame.quit()
                        block_data = get_block()
                        block_left_top = BLOCK_START_POINT[:]
                    elif event.key == pygame.K_LEFT:
                        if can_move(block_data, [_block_left_top_x - 1, _block_left_top_y], map_data):
                            block_left_top[0] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if can_move(block_data, [_block_left_top_x + 1, _block_left_top_y], map_data):
                            block_left_top[0] += 1
                    elif event.key == pygame.K_SPACE:
                        test_rorate = rorate_block(block_data)
                        #print_block(test_rorate)
                        if can_move(test_rorate, block_left_top, map_data):
                            block_data = test_rorate


            #print 'can_move: %s' % can_move(block_data,block_left_top,map_data)
            #print_block(map_data)
            screen.fill(BACKGROUND_COLOR)
            draw(block_data, block_left_top, map_data, screen)
            pygame.display.update()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()



