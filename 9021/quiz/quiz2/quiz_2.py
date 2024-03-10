# Written by *** and Eric Martin for COMP9021


def rule_encoded_by(rule_nb):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    '''
    values = [int(d) for d in f'{rule_nb:04b}']
    return {(p // 2, p % 2): values[p] for p in range(4)}
'''
    if (rule_nb>15)|(rule_nb<0)|(not isinstance(rule_nb,int)):
        print('please insert a int number between 0 and 15')
    else:
        rule_dict = {}
        d = rule_nb
        d = f'{d:04b}'
        rule_dict[(0,0)]= int(d)//1000
        rule_dict[(0,1)]= int(d)%1000//100
        rule_dict[(1,0)]= int(d)%1000%100//10
        rule_dict[(1,1)]= int(d)%10
        return(rule_dict)    
'''
    
    

def describe_rule(rule_nb):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    '''
    if (rule_nb>15)|(rule_nb<0)|(not isinstance(rule_nb,int)):
        print('plesae insert a int number between 0 and 15')
    else :
        rule = rule_encoded_by(rule_nb)
        print('The rule encoded by', rule_nb, 'is: ', rule)
        print('')
        for key in rule :
            print(f'After {key[0]:} followed by {key[1]:}, we draw {rule[key]:}')


def draw_line(rule_nb, first, second, length):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    "first" and "second" are supposed to be the integer 0 or the integer 1.
    "length" is supposed to be a positive integer (possibly equal to 0).

    
    Draws a line of length "length" consisting of 0's and 1's,
    that starts with "first" if "length" is at least equal to 1,
    followed by "second" if "length" is at least equal to 2,
    and with the remaining "length" - 2 0's and 1's determined by "rule_nb".
    '''

    if (rule_nb>15)|(rule_nb<0)|(not isinstance(rule_nb,int)) :
        print('plesae insert a int number between 0 and 15')
    else :
        rule = rule_encoded_by(rule_nb)
        a = first
        b = second
        list_t = []
        list_t.append(int(a))
        list_t.append(int(b))
        c = int(length)
        value=''
        if c==1:
            return print(list_t[0])
        elif c==2:
            return print(f'{list_t[0]}{list_t[1]}')
        elif c == 0 :
            return print("")
        elif c >2 :
            for m in range(c-2):
                key=(list_t[m],list_t[m+1])
                list_t.append(rule[key])
            for n in list_t :
                value += str(n)
            return print(value)

            

                
def uniquely_produced_by_rule(line):
    '''
    "line" is assumed to be a string consisting of nothing but 0's and 1's.

    Returns an integer n between 0 and 15 if the rule encoded by n is the
    UNIQUE rule that can produce "line"; otherwise, returns -1.
    '''
    line_1=str(line)
    a = len(line_1)
    b_dict = {}
    flag = 0 
    if a < 6 :
        flag = 1
    else :
        list_a = list(line_1)
        for i in range(a-2):
            key_b = (int(list_a[i]),int(list_a[i+1]))
            b_dict[key_b] = int(list_a[i+2])
        for key in b_dict :
            if type(b_dict[key])==list :
                flag = 1 
            elif len(b_dict) < 4 :
                flag = 1
            else:
                flag_1 = 0
                judge = 0
                for n in range(15):
                    rule = rule_encoded_by(n)
                    if b_dict == rule :
                        flag_1 = 1
                        return n
                    judge= judge +1
                    if flag_1 == 0 & judge == 15:
                        flag = 1
    if flag == 1:
        return -1
                
            
            
            
            
    
