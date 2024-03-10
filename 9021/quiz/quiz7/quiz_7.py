# Randomly fills a grid with True and False, with width, height and density
# controlled by user input, and computes the number of all "good paths" that link
# a point of coordinates (x1, y1) to a point of coordinates (x2, y2)
# (x1 and x2 are horizontal coordinates, increasing from left to right,
# y1 and y2 are vertical coordinates, increasing from top to bottom,
# both starting from 0), that is:
# - paths that go through nothing but True values in the grid
# - paths that never go through a given point in the grid more than once;
# - paths that never keep the same direction (North, South, East, West) over
#   a distance greater than 2.
#
# Written by *** and Eric Martin for COMP9021


from collections import namedtuple
import numpy as np 
from random import seed, randrange
import sys


Point = namedtuple('Point', 'x y')


def display_grid():
    for row in grid:
        print('   ', ' '.join(str(int(e)) for e in row))

def valid(pt):
    return 0 <= pt.x < width and 0 <= pt.y < height

def nb_of_good_paths(pt_1, pt_2):
    next_step = [[0,1],[0,-1],[1,0],[-1,0]]
    number_of_path = 0
    list_of_different_current_path = []
    list_of_different_current_path.append([pt_1.x, pt_1.y])
    if pt_1 == pt_2 :
        number_of_path =1
    elif (grid[pt_1.y][pt_1.x] == False) or (grid[pt_2.y][pt_2.x] == False):
        number_of_path = 0
    else:
        while list_of_different_current_path :
            current_path=[]
            current_path=list_of_different_current_path.pop(0)
            for step in next_step :
                if type(current_path[-1])==int :
                    current_path = [current_path]
                new_current_path = current_path.copy()
                current_step = new_current_path[-1]
                new_step = [0,0]
                new_step[0] = current_step[0] + step[0]
                new_step[1] = current_step[1] + step[1]
                if (0 <= new_step[0] <= width-1)and(0 <= new_step[1] <= height-1 )and(grid[new_step[1]][new_step[0]] == True)and([new_step[0],new_step[1]] not in new_current_path):
                    if len(current_path)>=3:
                        if current_path[-3][0]== current_path[-2][0] == current_path[-1][0] == new_step[0] :
                            continue
                        elif current_path[-3][1]== current_path[-2][1] == current_path[-1][1] == new_step[1] :
                            continue
                        else :
                            if new_step[0] == pt_2.x and new_step[1] == pt_2.y :
                                number_of_path += 1
                            else:
                                new_current_path.append([new_step[0],new_step[1]])
                                list_of_different_current_path.append(new_current_path)
                    else:
                        if new_step[0] == pt_2.x and new_step[1] == pt_2.y:
                            number_of_path += 1
                        else:
                            new_current_path.append([new_step[0], new_step[1]])
                            list_of_different_current_path.append(new_current_path)
    return number_of_path

# POSSIBLY DEFINE OTHER FUNCTIONS

try:
    for_seed, density, height, width = (abs(int(i)) for i in
                                                  input('Enter four integers: ').split()
                                       )
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
if not density:
    density = 1
seed(for_seed)
grid = np.array([randrange(density) > 0
                              for _ in range(height * width)
                ]
               ).reshape((height, width))
print('Here is the grid that has been generated:')
display_grid()
try:
    i1, j1, i2, j2 = (int(i) for i in input('Enter four integers: ').split())
    pt_1 = Point(i1, j1)
    pt_2 = Point(i2, j2)
    if not valid(pt_1) or not valid(pt_2):
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
print('Will compute the number of good paths '
      f'from ({pt_1.x}, {pt_1.y}) to ({pt_2.x}, {pt_2.y})...'
     )
paths_nb = nb_of_good_paths(pt_1, pt_2)
if not paths_nb:
    print('There is no good path.')
elif paths_nb == 1:
    print('There is a unique good path.')
else:
    print('There are', paths_nb, 'good paths.')
