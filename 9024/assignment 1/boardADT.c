//
// COMP9024 Assignment 1 - Sliding-Tile Puzzle
//
// Huiyao Zuo (z5196480@ad.unsw.edu.au)
//
// Written: 26/06/2019
//


#include "boardADT.h"


struct the_board {       // set the parameters of the board
    int *numbers ;        //use pointer to record the input numbers
    int size ;            //size
    int length ;        //length is the count of numbers
} ;


Board transfer_board(char *str) {
    Board board = malloc(sizeof(struct the_board)) ;           //create the memories for the board
    board->length = 0 ;                                        //initialize the length
    board->size = 0 ;                                          //initialize the size
    board->numbers = malloc(sizeof(int) * SIZE) ;              //create the space for the numbers
    char *str_line ;                                         //initialize the pointer of char to manage the input number
    int length_str = strlen(str) ;
    for (int i = 0 ; i < length_str ; i++) {
        if (*(str + i) == 'b') {                           //because the str will be saved as int ,so change the 'b' to number 0
            *(str + i) = '0' ;
        }
        if (!isdigit(*(str + i))) {                        //if other symbol mark in the line ,change to ' '
            (*(str + i)) = ' ' ;
        }
    }
    str_line = strtok(str, " ") ;                                //use strtok function to split the line
    while (str_line != NULL) {                                  //when all the number in the line is saved ,the str_line will be null
        *(board->numbers + board->length) = atoi(str_line) ;     //use the atoi function to transfer char to int
        board->length++ ;                                        //each time the number is saved ,the length need plus 1
        str_line = strtok(NULL, " ") ;                           //the str_line need point to next number
    }
    board->size = (int) sqrt(board->length) ;                    //calculate the size of the board
    return board ;
}

bool valid(Board board) {
    int len = board->length ;                                    //record the length
    int size = board->size ;                                     //record the size
    int value = size * size ;
    if (value == len) {                                         //size * size must equal to length
        if ((len >= 4) || (board->numbers != NULL)) {           //the smallest length is 4 and the numbers cannot be null
            for (int i = 0 ; i < len - 1 ; i++) {
                int count_repeat = 0;                                       //set the number to check the repeat number
                for (int j = i + 1 ; j < len ; j++) {
                    if (*(board->numbers + i) == *(board->numbers + j)) {
                        count_repeat++ ;
                    }
                    if (count_repeat >0) {                      //if the count_repeat  > 0 means there are same numbers in the input
                        return false ;
                    }
                }
            }
            return true ;
        }
    }
    return false ;
}

bool compare_board(Board board_start, Board board_goal){      //compare the numbers in two board
    int len = board_start ->length ;                          //get the length
    int count = 0 ;
    for (int i = 0 ; i < len ; i ++){
        int start = *(board_start->numbers + i);              //check the same number in one board before
        for (int j = 0 ; j < len ; j++){                      //compare the numbers in two board
            int goal = *(board_goal->numbers + j);
            if (start == goal){
                count ++ ;
            }
        }
    }
    if (count == len ){                                        //when the count equal to len ,mean the numbers in two board are same
        return true ;
    }
    else{
        return false ;
    }
}

int count_disorder(Board board) {
    int disorder = 0 ;                                         //Initialize the disorder number
    int size = board->size ;                                   //need the size because the odd and even size board is different
    int len = board->length ;
    if (size % 2 == 0) {                                      //calculate the disorder of the even board
        for (int i = len - 1 ; i >= 1 ; i--) {
            for (int j = i - 1 ; j >= 0 ; j--) {
                if (*(board->numbers + j) != 0 && *(board->numbers + i) != 0) {          //the number do not need to compare with 0
                    if (*(board->numbers + i) < *(board->numbers + j)) {            //calculate the disorder
                        disorder++ ;
                    }
                }
            }
        }
        for (int i = 0 ; i < len ; i++) {                      //find the 0 in which line
            if (*(board->numbers + i) == 0) {
                disorder += i / size + 1 ;
            }
        }
    } else {                                                 //calculate the disorder of the odd board
        for (int i = len - 1 ; i >= 1 ; i--) {
            for (int j = i - 1 ; j >= 0 ; j--) {
                if (*(board->numbers + j) != 0 &&
                    *(board->numbers + i) != 0) {            //the number do not need to compare with 0
                    if (*(board->numbers + i) < *(board->numbers + j)) {          //calculate the disorder
                        disorder++ ;
                    }
                }
            }
        }
    }
    return disorder ;
}

bool solvability_judge(Board board_start, Board board_goal) {
    int disorder_start = count_disorder(board_start) ;                      //get the disorder number of start board
    int disorder_goal = count_disorder(board_goal) ;                        //get the disorder number of goal board
    if (disorder_start % 2 == disorder_goal %2) {                          //when the two disorder number both odd or even the board is solvable
        return true ;
    }
    return false ;
}


void display_board(Board board) {                                 //display the board
    int len = board->length ;
    for (int i =0 ; i < len ; i ++){
        if (*(board->numbers + i) == 0){
            printf("b ") ;
        }
        else {
            printf("%d ", *(board->numbers + i)) ;
        }
    }
    printf("\n") ;
}


int board_length(Board board) {
    return board->length ;                         //return the length of the board
}


void free_the_board(Board board) {
    free(board->numbers) ;                        //free the memories created for the board
    free(board) ;
}
