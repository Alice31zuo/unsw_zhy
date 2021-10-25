import sys
import re
import os
from searchProblem import Arc, Search_problem
from searchGeneric import GreedySearcher
from cspProblem import CSP, Constraint
from display import Displayable
from cspConsistency import Search_with_AC_from_cost_CSP
import ast

domains = []

sentence = []

meeting_list = []

time_list = ['9am', '10am', '11am', '12pm', '1pm' , '2pm', '3pm', '4pm']

time_dict = {'9am':9, '10am': 10,'11am' : 11,'12pm' : 12,'1pm' :13 ,'2pm' :14 ,'3pm': 15,'4pm' : 16}

week_dict = {'mon':1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5}

week_list =  ['mon','tue','wed','thu','fri']



for i in week_list:
    for j in time_list:
        domains.append((i,j))  #get all the domain


csp_dic = {}                 #create dictionary
csp_func = []                #create list
csp_soft_func = []           #create list for soft function

######################################################

#hard function
def before_day(day):
    def before_day_x(x):
        key1 = x[0]
        key2 = day
        return week_dict[key1] < week_dict[key2]
    before_day_x.__name__ = 'before_day('
    return before_day_x

def before_time(time):
    def before_time_x(x):
        key1 = x[1]
        key2 = time
        return time_dict[key1] < time_dict[key2]
    before_time_x.__name__ = 'before_time('
    return before_time_x

def before_daytime(day,time):
    def before_daytime_x(x):
        key1 = x[0]
        key2 = day
        key3 = x[1]
        key4 = time
        return (week_dict[key1] < week_dict[key2] and time_dict[key3] < time_dict[key4])
    before_daytime_x.__name__ = 'before_daytime('
    return before_daytime_x


def after_day(day):
    def after_day_x(x):
        key1 = x[0]
        key2 = day
        return week_dict[key1] > week_dict[key2]
    after_day_x.__name__ = 'after_day('
    return after_day_x


def after_time(time):
    def after_time_x(x):
        key1 = x[1]
        key2 = time
        return time_dict[key1] > time_dict[key2]
    after_time_x.__name__ = 'after_time('
    return after_time_x


def after_daytime(day,time):
    def after_daytime_x(x):
        key1 = x[0]
        key2 = day
        key3 = x[1]
        key4 = time
        return (week_dict[key1] > week_dict[key2] and time_dict[key3] > time_dict[key4])
    after_daytime_x.__name__ = 'after_daytime('
    return after_daytime_x

def morning(x):            # finishes at or before 12pm
    key1 = x[1]
    return 9<=time_dict[key1]<=11


def afternoon(x):          # starts on or after 12pm
    key1 = x[1]
    return 12<=time_dict[key1]<=16


def day_time_day_time(day1,time1,day2,time2):
    def day_time_day_time_x(x):
        key1 = x[0]
        key2 = x[1]
        key3 = day1
        key4 = day2
        key5 = time1
        key6 = time2
        return  (week_dict[key3]<=week_dict[key1]<=week_dict[key4] and time_dict[key5]<=time_dict[key2]<=time_dict[key6])
    day_time_day_time_x.__name__ = 'day_time_day_time('
    return day_time_day_time_x


def only_day(day):
    def only_day_x(x):
        key1 = x[0]
        key2 = day
        return  week_dict[key1] == week_dict[key2]
    only_day_x.__name__ = 'only_day('
    return only_day_x

def only_time(time):
    def only_time_x(x):
        key1 = x[1]
        key2 = time
        return time_dict[key1] == time_dict[key2]
    only_time_x.__name__ = 'only_time('
    return only_time_x

######################################################
#binary constraints

def before(m1,m2):
    key1 = m1[0]
    key2 = m2[0]
    key3 = m1[1]
    key4 = m2[1]
    return (week_dict[key1] <= week_dict[key2] and time_dict[key3] < time_dict[key4])


def same_day(m1,m2):
    key1 = m1[0]
    key2 = m2[0]
    return (week_dict[key1] == week_dict[key2])



def one_day_between(m1,m2):
    key1 = m1[0]
    key2 = m2[0]
    return (abs(week_dict[key1] - week_dict[key2])==2)


def one_hour_between(m1,m2):
    key1 = m1[1]
    key2 = m2[1]
    return (abs(time_dict[key1] - time_dict[key2])==2)

##########################################################
#soft constraints

def early_week(x):
    key1 = x[0]
    return abs(week_dict[key1]-1)

def late_week(x):
    key1 = x[0]
    return abs(week_dict[key1]-5)

def early_morning(x):
    key1 = x[1]
    return abs(time_dict[key1]-9)

def midday(x):
    key1 = x[1]
    return abs(time_dict[key1]-12)

def late_afternoon(x):
    key1 = x[1]
    return abs(time_dict[key1]-16)


##########################################################


class softConstraint(object):

    def __init__(self, scope, condition):
        self.scope = scope
        self.condition = condition

    def __repr__(self):

        return self.condition.__name__ + str(self.scope)

    def count(self,assignment):

        return self.condition(*tuple(assignment[v] for v in self.scope))


class extendCSP(object):  #need add the soft
    def __init__(self, domains, constraints, softConstraint):
        """domains is a variable:domain dictionary
        constraints is a list of constriants
        """
        self.variables = set(domains)
        self.domains = domains
        self.constraints = constraints
        self.softConstraint = softConstraint
        self.var_to_const = {var: set() for var in self.variables}
        self.var_to_soft_const = {var_soft: set() for var_soft in self.variables}
        for con in constraints :
            for var in con.scope :
                self.var_to_const[var].add(con)
        for soft_con in softConstraint :
            for var_soft in soft_con.scope :
                self.var_to_soft_const[var_soft].add(soft_con)

    def __str__(self):
        """string representation of CSP"""
        return str(self.domains)

    def __repr__(self):
        """more detailed string representation of CSP"""
        return "CSP(" + str(self.domains) + ", " + str([str(c) for c in self.constraints]) + ")"

    def consistent(self, assignment):
        """assignment is a variable:value dictionary
        returns True if all of the constraints that can be evaluated
                        evaluate to True given assignment.
        """
        return all(con.holds(assignment)
                   for con in self.constraints
                   if all(v in assignment for v in con.scope))
    def cost(self,var,val):
        cost_number = 0
        for soft_con in self.var_to_soft_const[var] :
            cost_number += soft_con.count({var:val})
        return cost_number

    def heuristic(self,domains):
        if domains is None :
            domains = self.domains
        heuristic_num = 0
        for var in domains:
            min_cost = 10000
            for val in domains[var]:
                cost_num = self.cost(var,val)
                min_cost = min(min_cost,cost_num)
            heuristic_num += min_cost
        return heuristic_num


####################################################################



with open(sys.argv[1], "r")as file:  #read the file
    for line in file :
        if line == '\n':
            continue
        if '#' in line :
            continue
        txt = line.replace(',','')
        txt = txt.replace('\n', '')
        txt_all = re.split(' ',txt)
        sentence.append(txt_all)    #get all the sentence

for line in sentence:               #get all the meeting
    if 'meeting' in line[0]:
        meeting1 = line[1]
        meeting_list.append(meeting1)

for meeting in meeting_list :       #give the all domains to every meeting
    key = meeting
    csp_dic[key] = domains


######################################################


for line in sentence :
    if 'meeting' in line[0] :
        continue
    if 'constraint' in line[0]:          # binary constraints
        meeting1 = line[1]
        meeting2 = line[3]
        if 'before' in line[2]:
            func = Constraint((meeting1,meeting2), before)
            csp_func.append(func)
        elif 'same-day' in line[2]:
            func = Constraint((meeting1, meeting2), same_day)
            csp_func.append(func)
        elif 'one-day-between' in line[2]:
            csp_func.append(Constraint((meeting1, meeting2), one_day_between))
        else:                            #'one-hour-between' in line[1]:
            csp_func.append(Constraint((meeting1, meeting2), one_hour_between))

    else:                                #hard and soft constraints
        meeting = line[1]
        if 'hard' in line[-1]:           #hard condition
            if 'morning' in line[2]:
                csp_func.append(Constraint((meeting,),morning))

            elif 'afternoon' in line[2]:
                csp_func.append(Constraint((meeting,), afternoon))

            elif 'before' in line[2]:
                if len(line)==5:
                    if line[3] in week_list :
                        csp_func.append(Constraint((meeting,), before_day(line[3])))
                    else :
                        csp_func.append(Constraint((meeting, ), before_time(line[3])))
                else:
                    csp_func.append(Constraint((meeting,), before_daytime(line[3],line[4])))


            elif 'after' in line[2]:
                if len(line)==5:
                    if line[3] in week_list :
                        csp_func.append(Constraint((meeting,), after_day(line[3])))
                    else :
                        csp_func.append(Constraint((meeting,),after_time(line[3])))
                else:
                    csp_func.append(Constraint((meeting,), after_daytime(line[3],line[4])))


            elif len(line)==6 and ('before' not in line) and ('after' not in line) :
                time = re.split('-', line[3])
                csp_func.append(Constraint((meeting,), day_time_day_time(line[2],time[0],time[1],line[4])))

            else :                             #only time condition day time and daytime
                if line[2] in time_list :      #only time
                    csp_func.append(Constraint((meeting,), only_time(line[2])))
                else:
                    csp_func.append(Constraint((meeting,), only_day(line[2])))

        else:                                  #soft condition
            if 'early-week' in line[2]:
                csp_soft_func.append(softConstraint((meeting,), early_week))

            elif 'late-week' in line[2]:
                csp_soft_func.append(softConstraint((meeting,), late_week))

            elif 'early-morning' in line[2]:
                csp_soft_func.append(softConstraint((meeting,), early_morning))

            elif 'midday' in line[2]:
                csp_soft_func.append(softConstraint((meeting,), midday))

            else:
                csp_soft_func.append(softConstraint((meeting,), late_afternoon))


csp= extendCSP(csp_dic,csp_func,csp_soft_func)
searcher_csp = GreedySearcher(Search_with_AC_from_cost_CSP(csp))
solution = searcher_csp.search()                #get the solution
way = (str(solution).split("-->")[-1])          #get the path
node_1 = ast.literal_eval(way.replace(" ",""))  #get the node
way = way.replace('{','')
way = way.replace('}','')
way = way.replace(':','')
way = way.replace(',','')
way = way.replace('(','')
way = way.replace(')','')
way = way.replace('\'','')
word_way = re.split(' ',way)
del(word_way[0])
count_word = 0
if (node_1 == None) or (node_1 == {}):
    print("No solution", end="\n")
    sys.exit()
else:
    for i in range(len(word_way)):
        if (count_word == 0):
            print(word_way[i], end=":")
        elif (count_word == 1):
            print(word_way[i], end=" ")
        else:
            print(word_way[i], end="\n")
        count_word += 1
        if (count_word == 3):
            count_word = 0
    cost = csp.heuristic(node_1)
    print('cost:', cost, sep="", end="\n")
    sys.exit()





