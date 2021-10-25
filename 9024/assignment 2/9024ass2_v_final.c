//
// 9024 assignment 2
//
// z5196480
//

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>
#include "Graph.h"

int count_print = 1;

bool differByOne(char *first, char *second) {               //  the function to ensure two words only differ one
    int diff_num = strlen(second) - strlen(first);          //  get the length difference
    int count = 0;                                          //  set a count
    if (diff_num == 0) {                                    //  when two words equal
        for (int i = 0; i < strlen(first); i++) {           //  count how many  alpha differ
            if (*(first + i) != *(second + i)) {            //  when differ count+1
                count++;
                if (count == 2) {                           //  when count=2 mean two alpha differ
                    return false;                           //  and is false
                }
            }
        }
        return true;                                           //  else is true
    }
    else if (diff_num == 1) {                                  //  when two words not equal
        int lenght_1 = strlen(first) ;                         //  get the length of first
        int lenght_2 = strlen(second) ;                        //  get the length of second
        int m = 0 ;                                            //  set a m to compare the alpha
        while(*(first + m) == *(second + m)){                  //  count the same alpha
            count ++ ;
            m++ ;
        }
        while(*(first + lenght_1) == *(second + lenght_2)){    //  count the same alpha
            count ++ ;
            lenght_1 -- ;
            lenght_2 -- ;
        }
        count --;                                              //  get the right count
        if(count == strlen(first)){                            //  when same alpha number equal to first
            return true;                                       //  means true
        }
        else{
            return false;                                      //  if not mean false
        }
    }
    else{                                                      //  when diff_num >1 ,means false
        return false;
    }
}

void print_the_ladder(int total_length,int path_num, int left_num , int now_index  ,int *word_index ,const int (*num)[total_length], const char (*words)[50]){
    if (left_num ==2){                                             //  when the left_num =2 we can find the last word and  print them
        int i = now_index;                                         //  get the new line value
        for (int j = i+1 ; j<total_length ; j++){                  //  j must > i because only one direction
            if(num[i][j]==left_num){                               //  find  the last word
                int index_word = path_num - left_num +1 ;          //  get the index of word in the word_index list
                word_index[index_word] = j;
            }
        }
        printf(" %d: ",count_print) ;                              //  print order
        count_print ++ ;                                           //  order plus one
        for(int i = 0 ; i <path_num ; i ++){
            if (i == path_num-1 ){                                 //  print the last word
                printf("%s\n",words[word_index[i]]) ;
            }
            else{
                printf("%s -> ",words[word_index[i]]) ;            //  print word need add ->
            }
        }
        return ;
    }
    else{
        int i = now_index;                                         //  get the new line value
        for (int j = i+1 ; j<total_length ; j++){                  //  j must > i because only one direction
            if(num[i][j]==left_num){                               //  find  the word
                int index_word = path_num - left_num +1 ;          //  get the index of word in the word_index list
                word_index[index_word] = j;
                print_the_ladder(total_length,path_num, left_num -1 , j , word_index , num, words);  //  contine find the next word
            }
        }
    }
}


int main(int argc, char *argv[]) {
    char word[1000][50] ;                  //    set the array of words
    for(int i = 0 ; i< 1000 ; i++){        //    set the first is \0
        word[i][0] = '\0';
    }
    int index = 0 ;               //  set a index value of how many words
    int alpha = 0 ;               //  set a alpha value of how long words
    char input  = getchar() ;              //  get the input use getchar
    while (input != '\n'){                 //  when the input = EOF means the end
        if (isalpha(input)){                     //  ensure the input is alpha
            word[index][alpha] = input ;         //  put the input in the order of alpha
            alpha ++ ;                           //  alpha move to the next position
            word[index][alpha] = '\0' ;          //  next value set to \0 means the end of string
            input  = getchar();                  //  input get next value
        }
        else{                                       //  when input is not alpha means next word
            if(word[index] != word[index-1]){       //  insure the word is not same with before
                index ++ ;                          //  not same so index+1 means get next word
                alpha = 0 ;                         //  alpha to new word first position
                input  = getchar();                 //  input get next value
            }
            else{
                alpha = 0 ;                      //  means same words ,index not change
                input  = getchar();              //  input get next value
            }
        }
    }
    index ++ ;                                   //  index+1 means the total number of the word
    printf("Dictionary\n") ;                     //  print Dictionary
    for(int i = 0 ; i <index ; i++){                 // print words in order
        printf("%d: %s\n",i ,word[i]);
    }
    Graph graph_alpha = newGraph(index);             //  create Graph
    Edge edge;                                       //  create a edge to insert edge value
    for(int i = 0 ;i < index ; i ++){                      //  compare two words
    for (int j = i+1 ; j <index ; j++) {                   //  compare two words
            if (strlen(word[i]) > strlen(word[j])) {       //  insure the longer one's position
                if (differByOne(word[j], word[i])) {       //  judge the words relation
                    edge.v = i;                            //  get the edge value
                    edge.w = j;                            //  get the edge value
                    insertEdge(edge, graph_alpha);         //  insert the edge
                }
            } else {                                       //  insure the longer one's position
                if (differByOne(word[i], word[j])) {       //  judge the words relation
                    edge.v = i;                            //  get the edge value
                    edge.w = j;                            //  get the edge value
                    insertEdge(edge, graph_alpha);         //  insert the edge
                }
            }
        }
    }
    printf("Ordered Word Ladder Graph\n");         //  print Ordered Word Ladder Graph
    showGraph(graph_alpha);                        //  show Graph


   int index_longest_record[index] ;               //  set the array to get the largest point number
   for (int i = 0 ;i <index ; i++){                //  set all number to 1
       index_longest_record[i] = 1 ;
   }

   int dp_num_record[index][index] ;               //  the array to record the
   for (int i =0 ; i <index ; i++){                //  judge two words have edge or not
       for (int j = 0 ; j <index ;j++){
           dp_num_record[i][j] = 0 ;               //  set all number to 0
           edge.v = i;
           edge.w = j;
           if(isEdge(edge,graph_alpha)){           //  if in the edge  set the value to 1
               dp_num_record[i][j] = 1 ;
           }
       }
   }

   Edge edge_test;                                 //  create a edge to judge
   int the_num_path = 0 ;                          //  set the the_num_path to count largest path
    for(int array_row = index-2 ;array_row >=0 ; array_row --){                //  form the last to before
       int longest_num = 1 ;                                                   //  set the longest_num count the point in a path
       for (int array_col  = array_row +1 ; array_col <index ; array_col++){    //  only compare with the number smaller (in one direction)
           if(array_row != array_col){
               edge_test.v = array_row ;                                        //  get the edge value
               edge_test.w = array_col ;                                        //  get the edge value
               if (isEdge(edge_test,graph_alpha)){                              //  judge the egde in the graph
                   dp_num_record[array_row][array_col] = 1 + index_longest_record[array_col] ;        //  so the largest value need to plus one
                   if (dp_num_record[array_row][array_col] > longest_num){                            //  update the longest_num
                       longest_num = dp_num_record[array_row][array_col] ;
                   }
                }
           }
       }
       index_longest_record[array_row] = longest_num ;               //  get the index_longest_record[array_row] equal to longest_num
       if (longest_num > the_num_path){
           the_num_path = longest_num ;                              //  get the value of largest point in a path
       }
   }
    printf("Longest ladder length: %d\n",the_num_path);              //  print Longest ladder length:
/*
    for (int i =0 ; i <index ; i++){
        for (int j = 0 ; j <index ;j++){
            printf("%d ",dp_num_record[i][j]);
        }
        printf("\n");
    }

*/
    printf("Longest ladders:\n");              //  print Longest ladders:
    int array_word_index[1000];                //  set a array to record the index of word
    for (int i =0 ; i <index ; i++){           
        for (int j = i+1 ; j <index ;j++){
            if (dp_num_record[i][j] == the_num_path){    //find the start point of longest path
                array_word_index[0] = i ;                //record the index
                array_word_index[1] = j ;                //record the index
                print_the_ladder(index,the_num_path, the_num_path -1 , j , array_word_index , dp_num_record, word);  //  find the next word
            }
        }
    }
}
