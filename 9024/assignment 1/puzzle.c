//
// COMP9024 Assignment 1 - Sliding-Tile Puzzle
//
// Huiyao Zuo (z5196480@ad.unsw.edu.au)
//
// Written: 26/06/2019
//


#include "boardADT.h"

int main(int argc ,char **argv){
    char *start_text = malloc(sizeof(char)*SIZE) ;  //create the memories for start text
    char *goal_text = malloc(sizeof(char)*SIZE) ;   //create the memories for goal text
    fgets(start_text,SIZE,stdin) ;                  //use fgets function to get the start_text from stdin
    fgets(goal_text,SIZE,stdin) ;                   //use fgets function to get the goal_text from stdin


    Board board_start = transfer_board(start_text) ;  //get the start_board
    Board board_goal = transfer_board(goal_text) ;    //get the goal_board

    printf("start: ") ;
    display_board(board_start) ;                      //print the start_text
    printf("goal: ") ;
    display_board(board_goal) ;                       //print the goal_text

    if (board_length(board_start) != board_length(board_goal) || !valid(board_start) || \
    !valid(board_goal)|| !compare_board(board_start,board_goal)){
        printf("input error\n") ;                     // if the start board length not equal to goal board ,the input is wrong
        free(start_text) ;                           // and the two board need be valid ,and compare the numbers in two board are same
        free(goal_text) ;                                 // free the memories created for start_text ,free the memories created for goal_text
        free_the_board(board_start) ;                     //free the memories created for board_start
        free_the_board(board_goal) ;                      //free the memories created for goal_start
        return EXIT_FAILURE ;                         // if one of start board and goal board not valid ,the input is wrong
    }
    else{
        if(solvability_judge(board_start , board_goal)){  //judge the goal board is solvable or not
            printf("solvable\n") ;
        }
        else{
            printf("unsolvable\n") ;
        }
    }
    free(start_text) ;                                // free the memories created for start_text
    free(goal_text) ;                                 // free the memories created for goal_text
    free_the_board(board_start) ;                     // free the memories created for board_start
    free_the_board(board_goal) ;                      // free the memories created for goal_start

    return EXIT_SUCCESS ;
}
