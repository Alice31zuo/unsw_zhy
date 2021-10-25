//
// COMP9024 Assignment 1 - Sliding-Tile Puzzle
//
// Huiyao Zuo (z5196480@ad.unsw.edu.au)
//
// Written: 26/06/2019
//


#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>


#define SIZE 1024
//define the size to fast create the space

typedef struct the_board *Board ;
//set the struct the_board as a new type so that directly create the pointer to point the struct


Board transfer_board(char *str) ;
//the function is used to transfer the input number to a board
//return the board

void display_board(Board board);
//display the line


bool valid(Board board) ;
//this function is to valid the board weather fit in the numbers standard or not
//return true (valid) or false (not valid)

bool compare_board(Board board_start, Board board_goal);
//compare the numbers in two board
//return true (same) or false (not same)

int count_disorder(Board board) ;
//count the disorder number of the board
//return the disorder number of the board

bool solvability_judge(Board board_start , Board board_goal ) ;
//judge the board is solvable or not
//return true（solvable) or false（unsolvable)

int board_length(Board board) ;
//return the length of the board

void free_the_board(Board board);
//free the space created for the board


