# Prompts the user for a positive integer that codes a set S as follows:
# - Bit 0 codes 0
# - Bit 1 codes -1
# - Bit 2 codes 1
# - Bit 3 codes -2
# - Bit 4 codes 2
# - Bit 5 codes -3
# - Bit 6 codes 3
# ...
# Computes a derived positive integer that codes the set of running sums
# ot the members of S when those are listed in increasing order.
#
# Written by *** and Eric Martin for COMP9021


from itertools import accumulate
import sys

try:
    encoded_set = int(input('Input a positive integer: '))
    if encoded_set < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

# POSSIBLY DEFINE OTHER FUNCTIONS    
def display_encoded_set(encoded_set):
    if type(encoded_set)==int:
        length = len(bin(encoded_set)[2:])
        list_code = []
        encoded_set_code = []
        final_set =[]
        if encoded_set == 0 :
            print('{}')
        else:
            if encoded_set == 1 :
                list_code = [0]
            for e in range(1,length):
                if e == 1 :
                    list_code.append(0)
                if e % 2 ==0:
                    list_code.append(e/2)
                if e % 2 != 0:
                    list_code.append(-(e+1)/2) #获得标准列表
            list_number =[ int(e) for e in bin(encoded_set)[2:]]
            for i in range(length-1,-1,-1):
                encoded_set_code.append(list_number[i])
            for i in range(length):
                if encoded_set_code[i]==1:
                    final_set.append(int(list_code[i]))
            final_set = sorted(final_set)
            print('{',end = '')
            for i in range(len(final_set)):
                if i == len(final_set)-1:
                    print(final_set[i],end = '')
                else:
                    print(final_set[i],end = '')
                    print(',',end = ' ')
            print('}')
    elif type(encoded_set)==set:
        list_uncode = list(encoded_set)
        num = 0
        for i in list_uncode:
            if i < 0 :
                num = num + 2**(-i*2 - 1)
            if i > 0 :
                num = num +2**(i * 2)
            if i ==0:
                num = num + 1
        return(num)
    elif encoded_set == {}:
        return 0
    # REPLACE pass ABOVE WITH CODE TO PRINT OUT ENCODED SET (WITH print() STATEMENTS)

def code_derived_set(encoded_set):
    length = len(bin(encoded_set)[2:])
    list_code = []
    encoded_set_code = []
    final_set =[]
    if encoded_set == 0 :
        print('{}')
        return {}
    else:
        if encoded_set == 1 :
            list_code = [0]
        for e in range(1,length):
            if e == 1 :
                list_code.append(0)
            if e % 2 ==0:
                list_code.append(e/2)
            if e % 2 != 0:
                list_code.append(-(e+1)/2) #获得标准列表
        list_number =[ int(e) for e in bin(encoded_set)[2:]]
        for i in range(length-1,-1,-1):
            encoded_set_code.append(list_number[i])
        for i in range(length):
            if encoded_set_code[i]==1:
                final_set.append(int(list_code[i]))
        final_set = sorted(final_set)
        encoded_running_sum = sorted(set(accumulate(final_set)))
        print('{',end = '')
        for i in range(len(encoded_running_sum)):
            if i == len(encoded_running_sum) -1 :
                print(encoded_running_sum[i],end = '')
            else:
                print(encoded_running_sum[i],end = '')
                print(',',end=' ')
        print('}')
        return (set(encoded_running_sum))

print('The encoded set is: ', end = '')
display_encoded_set(encoded_set)
print('The derived encoded set is: ', end = '')
encoded_running_sum = code_derived_set(encoded_set)
num = display_encoded_set(encoded_running_sum)
print('  It is encoded by:', num)
'''

print('The encoded set is: ', end = '')
display_encoded_set(encoded_set)
encoded_running_sum = code_derived_set(encoded_set)
print('The derived encoded set is: ', end = '')
display_encoded_set(encoded_running_sum)
print('  It is encoded by:', encoded_running_sum)
'''
