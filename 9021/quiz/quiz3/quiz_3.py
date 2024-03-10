# Written by Eric Martin for COMP9021



import sys
from random import seed, randint, randrange


try:
    arg_for_seed, upper_bound, length =\
            (int(x) for x in input('Enter three integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()


def length_of_longest_increasing_sequence(L):
    length_L=len(L)
    li = 1
    a = 1
    b = 1
    for i in range(2*length_L):
        if L[li-1] <= L[li] :
            a += 1
            li += 1
            if li == length_L:
                if L[li-1] <= L[0]:
                    a += 1
                    li = 1
                if L[li-1] > L[0]:
                    if a > b :
                        b = a
                        a = 1
                        li = 1
                    else :
                        a = 1
                        li =1
        if L[li-1] > L[li] :
            if a > b :
                b = a
                a = 1
                li += 1
            else :
                a = 1
                li += 1
            if li == length_L:
                if L[li-1] <= L[0]:
                    a += 1
                    li = 1
                if L[li-1] > L[0]:
                    if a > b :
                        b = a
                        a = 1
                        li = 1
                    else :
                        a = 1
                        li =1
    return b


def max_int_jumping_in(L):
    str_s = ''
    str_t = ''
    length_l =len(L)
    list_site = []
    for i in range(length_l):
        site = i
        b = 0
        list_site.append(site)
        a = site
        str_s = str(L[a])
        while b == 0 :
            site = L[a]
            if site in list_site :
                b = 1 
            else:
                list_site.append(site)
                a = site
                str_s += str(L[a])
                b = 0
        if len(str_s) > len(str_t) :
            str_t = str_s
        if len(str_s) == len(str_t) & int(str_s)>int(str_t) :
            str_t = str_s
        list_site = []
    return (str_t)
    
            
            
    

        

seed(arg_for_seed)
L_1 = [randint(0, upper_bound) for _ in range(length)]
print('L_1 is:', L_1)
print('The length of the longest increasing sequence\n'
      '  of members of L_1, possibly wrapping around, is:',
      length_of_longest_increasing_sequence(L_1), end = '.\n\n'
     )
L_2 = [randrange(length) for _ in range(length)]
print('L_2 is:', L_2)
print('The maximum integer built from L_2 by jumping\n'
      '  as directed by its members, from some starting member\n'
      '  and not using any member more than once, is:',
      max_int_jumping_in(L_2)
     )


