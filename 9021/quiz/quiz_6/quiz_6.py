# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and determines the size of the largest
# isosceles triangle, consisting of nothing but 1s and whose base can be either
# vertical or horizontal, pointing either left or right or up or down.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import numpy as np
import sys


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))

def size_of_largest_isosceles_triangle(a):
    list_test = a
    count_list = []
    for i in range(10):
        for j in range(10):
            count = 0
            add_row = 0
            add_column = 0
            if list_test[i][j] != 0 :
                count += 1
                while ((i+1+add_row) in range(10))and ((j-1-add_column) in range(10)) and((j+2+add_column) in range(10)) and all(list_test[i+1+add_row][j-1-add_column:j+2+add_column]) != 0 :
                    count += 1
                    add_row += 1
                    add_column +=1
                    if (j+2+add_column ==10) and ((i+1+add_row) in range(10))and ((j-1-add_column) in range(10)) and all(list_test[i+1+add_row][j-1-add_column:j+2+add_column]) != 0 :
                        count += 1
                        add_row += 1
                        add_column += 1
            count_list.append(count)
    return(max(count_list))

                    # REPLACE pass WITH YOUR CODE

# POSSIBLY DEFINE OTHER FUNCTIONS

try:
    arg_for_seed, density = (abs(int(x)) for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()
max_size_final = 1
count_final = [0]
grid_90_1 = np.rot90(grid,1)
grid_90_2 = np.rot90(grid,2)
grid_90_3 = np.rot90(grid,3)
count_final.append(size_of_largest_isosceles_triangle(grid))
count_final.append(size_of_largest_isosceles_triangle(grid_90_1))
count_final.append(size_of_largest_isosceles_triangle(grid_90_2))
count_final.append(size_of_largest_isosceles_triangle(grid_90_3))
max_size_final = max(count_final)
print('The largest isosceles triangle has a size of',
      max_size_final
     )
