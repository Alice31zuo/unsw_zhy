import re
from collections import defaultdict
import copy

def available_coloured_pieces(file):
    list_path = []
    for line in file:
        if 'path' in str(line):
            list_path.append(str(line))
    return list_path

def are_valid(file):
    list_path = file
    list_number = []
    judge = 0
    for path in list_path:
        list_number = re.findall(r"[0-9]+", path)
        length = len(list_number)
        num_of_point = int(length/2)
        list_of_point = []
        count = num_of_point
        for i in range(num_of_point):
            if i == 0:
                list_of_point.append([int(list_number[i]), int(list_number[i + 1])])
            else:
                list_of_point.append([int(list_number[2 * i]), int(list_number[2 * i + 1])])
        #得到了所有的点的坐标
        #开始对点进行分析原理是除了自身以外所有的点都大于零或者小于零
        for m in range(num_of_point):
            for n in range(num_of_point):
                if m == n :
                    continue
                else:
                    if list_of_point[m] == list_of_point[n]:
                        return False
        while count-1 >= 0 :
            list_of_judge = []
            judge_num = 0
            if count-1 == 0 :
                for i in range(num_of_point):
                    if (i == 0) or (i == num_of_point-1):
                        continue
                    else:
                        equation_of_x = list_of_point[i][0] - list_of_point[0][0]
                        equation_of_1_x = list_of_point[num_of_point-1][0] - list_of_point[0][0]
                        equation_of_y = (list_of_point[i][1] - list_of_point[0][1])
                        equation_of_1_y = list_of_point[num_of_point-1][1] - list_of_point[0][1]
                        if equation_of_1_x == 0 :
                            judge_num = list_of_point[i][0] - list_of_point[0][0]
                            list_of_judge.append(judge_num)
                        elif equation_of_1_y == 0 :
                            judge_num = list_of_point[i][1] - list_of_point[0][1]
                            list_of_judge.append(judge_num)
                        else:
                            judge_num = equation_of_x/equation_of_1_x - equation_of_y/equation_of_1_y
                            list_of_judge.append(judge_num)
                for m in range(len(list_of_judge)):
                    for n in range(len(list_of_judge)):
                        if (list_of_judge[m]<0 and list_of_judge[n]>0) or(list_of_judge[m]>0 and list_of_judge[n]<0):
                            judge = 1
                if judge != 0:
                    return False
                list_of_judge = []
                judge_num = 0

#                if not (all(list_of_judge) < 0 or all(list_of_judge) > 0): all不是这么用的
            else:
                for i in range(num_of_point) :
                    if (i == count-1) or (i ==count -2) :
                        continue
                    else:
                        equation_of_x = list_of_point[i][0]-list_of_point[count-1][0]
                        equation_of_1_x = list_of_point[count-2][0]-list_of_point[count-1][0]
                        equation_of_y = list_of_point[i][1]-list_of_point[count-1][1]
                        equation_of_1_y = list_of_point[count-2][1]-list_of_point[count-1][1]
                        if equation_of_1_x == 0 :
                            judge_num = list_of_point[i][0] - list_of_point[count-1][0]
                            list_of_judge.append(judge_num)
                        elif equation_of_1_y == 0 :
                            judge_num = list_of_point[i][1] - list_of_point[count-1][1]
                            list_of_judge.append(judge_num)
                        else:
                            judge_num = equation_of_x/equation_of_1_x - equation_of_y/equation_of_1_y
                            list_of_judge.append(judge_num)
                for m in range(len(list_of_judge)):
                    for n in range(len(list_of_judge)):
                        if (list_of_judge[m] < 0 and list_of_judge[n] > 0) or (list_of_judge[m] > 0 and list_of_judge[n] < 0):
                            judge = 1
                if judge != 0:
                    return False
                list_of_judge = []
                judge_num = 0
            count -= 1
    if judge == 0:
        return True
    else:
        return False
    

def rotate_the_pices(list_1): #测试通过
    #这里可以先把对应的点和坐标求出来，然后求对应的向量，最终我们比价的是向量，但是最后也有可能是相反的方向，所以每一个相反的向量也有求一遍
    #首先因为所有的点都在第一象限，所以我们找到第二，第三，第四象限的图形和向量，并得到它相反的向量。
    #第一象限转第二象限
    dict_path = defaultdict()
    for m in range(len(list_1)):
        path_number = []
        path_point_1= []
        path_four_point = []
        path_number = re.findall(r"[0-9]+", list_1[m])
        for i in range(int(len(path_number) / 2)):  # 得到了所有的点
            if i == 0:
                path_point_1.append([int(path_number[i]), int(path_number[i + 1])])
            else:
                path_point_1.append([int(path_number[2 * i]), int(path_number[2 * i + 1])])
        path_four_point.append(path_point_1) #得到第一象限的点
        path_point_2 = copy.deepcopy(path_point_1)
        path_point_3 = copy.deepcopy(path_point_1)
        path_point_4 = copy.deepcopy(path_point_1)
        path_point_5 = copy.deepcopy(path_point_1) #将坐标按y=x轴翻转
        path_point_6 = copy.deepcopy(path_point_1)
        for i in range(len(path_point_2)):
            #得到第二象限的点
            a = path_point_2[i][0]
            path_point_2[i][0] = 0 - a #第二象限x值相反，但是y相等
        path_four_point.append(path_point_2) #得到第二象限的点
        for i in range(len(path_point_3)):
            #得到第三象限的点
            a = path_point_3[i][0]
            b = path_point_3[i][1]
            path_point_3[i][0] = 0 - a
            path_point_3[i][1] = 0 - b
        path_four_point.append(path_point_3) #得到第三象限的点
        for i in range(len(path_point_4)):
            # 得到第四象限的点
            a = path_point_4[i][1]
            path_point_4[i][1] = 0 - a  # 第四象限x值相等，但是y相反
        path_four_point.append(path_point_4)  # 得到第四象限的点
        for i in range(len(path_point_5)):
            # 得到y=x的点
            a = path_point_5[i][0]
            b = path_point_5[i][1]
            path_point_5[i][0] = b
            path_point_5[i][1] = a  #将x ， y 的值对调
        path_four_point.append(path_point_5)  # 得到y=x的点
        for i in range(len(path_point_6)):
            # 得到y=-x的点
            a = path_point_6[i][0]
            b = path_point_6[i][1]
            path_point_6[i][0] = 0 - b
            path_point_6[i][1] = 0 - a  #将x ， y 的值对调
        path_four_point.append(path_point_6)  # 得到第四象限的点
        #因为只需要向量，并不需要点，所以存储的字典里面不需要字典
        #然后计算向量的值，存储在字典里
        path_vector = []
        for n in range(6):
            single_vector = [] #这里已经有了
            for i in range(len(path_four_point[n])):
                if i == 0:
                    single_vector.append([path_four_point[n][i][0]-path_four_point[n][len(path_four_point[n])-1][0], \
                                        path_four_point[n][i][1]-path_four_point[n][len(path_four_point[n])-1][1]])
                else:
                    single_vector.append([path_four_point[n][i][0]-path_four_point[n][i-1][0], \
                                        path_four_point[n][i][1]-path_four_point[n][i-1][1]])
            path_vector.append(single_vector) #这里就得到了每个象限的向量
        #完成循环之后就得到了所有象限的向量，然后存储在字典里面
        key = m
        dict_path[key]= path_vector#这里就得到了所有方块四个方向的向量
    return dict_path
        #然后就开始比较了

def revers_the_pices(list_2): #测试通过
    dict_path = defaultdict()
    for m in range(len(list_2)):
        path_number = []
        path_point= []
        path_number = re.findall(r"[0-9]+", list_2[m])
        for i in range(int(len(path_number) / 2)):  # 得到了所有的点
            if i == 0:
                path_point.append([int(path_number[i]), int(path_number[i + 1])])
            else:
                path_point.append([int(path_number[2 * i]), int(path_number[2 * i + 1])])
        path_vector = []
        vector = []
        for i in range(len(path_point)) :#得到顺时针的向量
            if i == 0:
                vector.append([path_point[i][0]-path_point[len(path_point)-1][0], \
                                    path_point[i][1]-path_point[len(path_point)-1][1]])
            else:
                vector.append([path_point[i][0]-path_point[i-1][0], \
                                    path_point[i][1]-path_point[i-1][1]])
        path_vector.append(vector) #得到向量
        vector = []
        for i in range(len(path_point)-1,-1,-1) :#得到逆时针的向量
            if i == len(path_point)-1:
                vector.append([path_point[len(path_point)-1][0]-path_point[0][0], \
                                    path_point[len(path_point)-1][1]-path_point[0][1]])
            else:
                vector.append([path_point[i][0]-path_point[i+1][0], \
                                    path_point[i][1]-path_point[i+1][1]])
        path_vector.append(vector)
        key = m
        dict_path[key]= path_vector#这里就得到了两个方向的向量
    return dict_path

#'''
def find_the_sequence_path(dic_path_2): #测试通过
    for key in dic_path_2:
        for m in range(2):
            list = copy.deepcopy(dic_path_2[key][m])
            for n in range(len(dic_path_2[key][m])-1):
                a = list.pop(0)
                list.append(a)
                dic_path_2[key].append(copy.deepcopy(list)) #得到所有的排序的向量序列
    return dic_path_2

#'''

#'''
def are_identical_sets_of_coloured_pieces(list_1,list_2):
    if len(list_1) != len(list_2):
        return False
    else:
        dict_path_1 = rotate_the_pices(list_1)
        dict_path_2 = revers_the_pices(list_2)
        dict_path_2 = find_the_sequence_path(dict_path_2)
        length_ture = len(list_2)
        count_path_1 = []
        count_path_2 = []
        #需要考虑变换的顺序怎么样？要不再写一个函数？把所有的情况都列出来？这个对dictpath——2进行处理？
 #       ''''
        for key_2 in dict_path_2:
            for m in range(len(dict_path_2[key_2])):
                for key_1 in dict_path_1:
                    for n in range(len(dict_path_1[key_1])):
                        if dict_path_2[key_2][m] == dict_path_1[key_1][n] :
                            count_path_1.append(key_1)
                            count_path_2.append(key_2)
        count_path_1 = list(set(count_path_1))
        count_path_2 = list(set(count_path_2))
        if len(count_path_1) == len(count_path_2) == length_ture:
            return True
        else:
            return False

def is_solution(tangram, shape):
    return False
    

