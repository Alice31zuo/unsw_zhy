import re
import os
import sys
from collections import defaultdict


def analyse_the_sentence(list_1,list_2,list_3):
	#the_posible_list：是一个二维数组，list_speaker_content是一个二维数组
	#注意，还要找到说话人是1 还是 0 ，然后在判断函数里写出如果这个人是1的需要删除的列表，如果这个人是0的时候需要删除的列表，就可以同时删除两个部分
	#这里给的list_speaker_content 必须只能是一对，就是一个人和一个句子，不然还要写一个大循环
    people_name_1 = []
    people_index_list = list_1 
    the_posible_list = list_2
    num_of_people = len(people_index_list)
    content_sentence = list_3 #这里应该是一个二维数组，最好把之前的句子的list清理一下，只留说话的人和内容
	#list_speaker_content[0] 是人，list_speaker_content[1]是句子 ，句子改到在外部循环
    for name in people_index_list :
        if name in content_sentence[0] :
            people_name_1.append(people_index_list.index(name))#这里就找到了说话的人
    speaker_index = people_name_1[0]
  #  speaker_index = people_index_list.index(people_name_1) #这里得到了说话人的index
    list_index = []
    for name in people_index_list:
        if name in sentence[1]:
            index = people_index_list.index(name)
            list_index.append(index)
        num_of_people_and = len(list_index)
#    print(the_posible_list)
    for i in range(len(the_posible_list)):
        value_of_judege = 0
        for value in the_posible_list[i]:
            value_of_judege += value
        value_of_judege_and = 0
        for value in list_index:
            value_of_judege_and += the_posible_list[i][value]
#        print(the_posible_list)
        speaker_trueth = the_posible_list[i][speaker_index]
        value_of_judege_and_I = value_of_judege_and + speaker_trueth
        num_of_people_and_I = num_of_people_and + 1
        if len(the_posible_list[i]) == 0 : 
            return the_posible_list
        else :
            if (('At ' in sentence[1]) |('at ' in sentence[1] ))&('least ' in sentence[1]) &('one ' in sentence[1] )& (('and ' in sentence[1] )|('us 'in sentence[1]))&('is ' in sentence[1]) & ((' Knight'in sentence[1])|(' Knave'in sentence[1])):
                if 'us ' in sentence[1]:
                    if ' Knight' in sentence[1]:# 再在这里加上当人为几的时候的判断
                #	if value_of_judege >=1: #此条语句正确的输出，但我们是要排除错误的列表
                        if speaker_trueth  == 1 :
                            if value_of_judege == 0 : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege >= 1 : 
                                the_posible_list[i] = []

                    if ' Knave' in sentence[1]:
                                #此时满足条件的正确输出为 value_of_judege <= num_of_people - 1
                        if speaker_trueth  == 1 :
                            if value_of_judege == num_of_people : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege <= num_of_people-1 : 
                                the_posible_list[i] = []

                if 'and ' in sentence[1]:
                    if 'I ' in sentence[1]:
                        if ' Knight' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and_I == 0 : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and_I >= 1 : 
                                    the_posible_list[i] = []
                        if ' Knave' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and_I == num_of_people_and_I : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and_I <= num_of_people_and_I - 1 : 
                                    the_posible_list[i] = []
                    else:
                        if ' Knight' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and == 0 : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and >= 1 : 
                                    the_posible_list[i] = []
                        if ' Knave' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and == num_of_people_and : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and <= num_of_people_and-1 : 
                                    the_posible_list[i] = []
                        #第一种情况完成
            if (('At 'in sentence[1])|('at ' in sentence[1]))&('most 'in sentence[1])&('one 'in sentence[1])&(( 'and 'in sentence[1])|('us 'in sentence[1]))&('is 'in sentence[1])&((' Knight'in sentence[1])|(' Knave'in sentence[1])) :
                if 'us ' in sentence[1]:
                    if ' Knight' in sentence[1]:
                        if speaker_trueth  == 1 :
                            if value_of_judege > 1 : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege <= 1 : 
                                the_posible_list[i] = []
                    if ' Knave' in sentence[1]:
                        if speaker_trueth  == 1 :
                            if value_of_judege < num_of_people - 1: 
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege >= num_of_people - 1 : 
                                the_posible_list[i] = []
                if 'and ' in sentence[1]:
                    if 'I ' in sentence[1]:
                        if ' Knight' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and_I > 1  : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and_I <=1 : 
                                    the_posible_list[i] = []
                        if ' Knave' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and_I < num_of_people_and_I -1 : 
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and_I >= num_of_people_and_I - 1 : 
                                    the_posible_list[i] = []
                    else:
                        if ' Knight' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and > 1 : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and <= 1 : 
                                    the_posible_list[i] = []
                        if ' Knave' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and < num_of_people_and - 1: 
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and >= num_of_people_and - 1 : 
                                    the_posible_list[i] = []

            if (('Exactly 'in sentence[1])|('exactly ' in sentence[1]))&('one 'in sentence[1])&('and 'in sentence[1])|('us 'in sentence[1])&('is 'in sentence[1])&((' Knight'in sentence[1])|(' Knave'in sentence[1])):
                if 'us ' in sentence[1]:
                    if ' Knight' in sentence[1]:
                        if speaker_trueth  == 1 :
                            if value_of_judege != 1 : 
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege == 1 : 
                                the_posible_list[i] = []
                    if ' Knave' in sentence[1]:
                                #此时满足条件的正确输出为 value_of_judege == num_of_people - 1
                        if speaker_trueth  == 1 :
                            if value_of_judege != num_of_people-1 : 
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege == num_of_people-1 : 
                                the_posible_list[i] = []
                if 'and ' in sentence[1]:
                    if 'I ' in sentence[1]:
                        if ' Knight' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and_I !=1 : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and_I ==1 : 
                                    the_posible_list[i] = []
                        if ' Knave' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and_I != num_of_people_and_I -1: 
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and_I == num_of_people_and_I - 1 : 
                                    the_posible_list[i] = []
                    else:
                        if ' Knight' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and != 1 : 
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and == 1 : 
                                    the_posible_list[i] = []
                        if ' Knave' in sentence[1]:
                            if speaker_trueth  == 1 :
                                if value_of_judege_and != num_of_people_and -1 : 
                                    the_posible_list[i] = []
                            if speaker_trueth  == 0 :
                                if value_of_judege_and == num_of_people_and -1 : 
                                    the_posible_list[i] = []

            if (('All 'in sentence[1])|('all 'in sentence[1] ))&('us 'in sentence[1])&('are 'in sentence[1])&((' Knights'in sentence[1])|(' Knaves'in sentence[1])):
                if ' Knights' in sentence[1]:
                #	if value_of_judege == num_of_people: #此条语句正确的输出，但我们是要排除错误的列表
                    if speaker_trueth  == 1 :
                        if value_of_judege != num_of_people: 
                            the_posible_list[i] = []
                    if speaker_trueth  == 0 :
                        if value_of_judege == num_of_people : 
                            the_posible_list[i] = []
                if ' Knaves' in sentence[1]:
                #此时满足条件的正确输出为 value_of_judege == 0
                    if speaker_trueth  == 1 :
                        the_posible_list[i] = []
                    if speaker_trueth  == 0 :
                        if value_of_judege == 0 : 
                            the_posible_list[i] = []		
            if ('I 'in sentence[1])&(' am'in sentence[1])&('a 'in sentence[1])&((' Knight'in sentence[1])|(' Knave'in sentence[1])) :
                if ' Knave' in sentence[1]:  #找说话的人
                    the_posible_list[i] = []	

            if  ('Sir 'in sentence[1])&('a 'in sentence[1])&((' Knight'in sentence[1])|(' Knave'in sentence[1]))&('I ' not in sentence[1])&('one ' not in sentence[1]):
                if ' Knight' in sentence[1]: #找说话的人
                    if speaker_trueth  == 1 :
                        if the_posible_list[i][list_index[0]] != 1: 
                            the_posible_list[i] = []
                    if speaker_trueth  == 0 :
                        if the_posible_list[i][list_index[0]] == 1 : 
                            the_posible_list[i] = []
                if ' Knave' in sentence[1]:  #找说话的人
                    if speaker_trueth  == 1 :
                        if the_posible_list[i][list_index[0]] != 0: 
                            the_posible_list[i] = []
                    if speaker_trueth  == 0 :
                        if the_posible_list[i][list_index[0]] == 0 : 
                            the_posible_list[i] = []	

            if  ('or 'in sentence[1])&('a 'in sentence[1])&((' Knight'in sentence[1])|(' Knave'in sentence[1])):
                if ' Knight' in sentence[1]:
                    if speaker_trueth  == 1 :
                        if value_of_judege_and != 1 : 
                            the_posible_list[i] = []
                    if speaker_trueth  == 0 :
                        if value_of_judege_and == 1 : 
                            the_posible_list[i] = []
                if ' Knave' in sentence[1]: 
                    if speaker_trueth  == 1 :
                        if value_of_judege_and != num_of_people_and - 1 :
                            the_posible_list[i] = []
                    if speaker_trueth  == 0 :
                        if value_of_judege_and == num_of_people_and - 1 : 
                            the_posible_list[i] = []

            if  ('and 'in sentence[1])&('are 'in sentence[1])&((' Knights'in sentence[1])|(' Knaves'in sentence[1])):
                if ' Knights' in sentence[1]: #找说话的人
                    if  'I ' in sentence[1]:
                        if speaker_trueth  == 1 :
                            if value_of_judege_and_I != num_of_people_and_I : #之后在这里判断的时候加上当人的数据是零或者一的情况
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege_and_I == num_of_people_and_I : 
                                the_posible_list[i] = []
                    else:
                        if speaker_trueth  == 1 :
                            if value_of_judege_and != num_of_people_and  : 
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege_and == num_of_people_and  : 
                                the_posible_list[i] = []
                if ' Knaves' in sentence[1]:  #找说话的人
                    if  'I ' in sentence[1]:
                        if speaker_trueth  == 1 :
                            the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege_and_I == 0  : 
                                the_posible_list[i] = [] 
                    else:
                        if speaker_trueth  == 1 :
                                the_posible_list[i] = []
                        if speaker_trueth  == 0 :
                            if value_of_judege_and == 0  : 
                                the_posible_list[i] = []
    return (the_posible_list)

##################################################################################################################
filename = input('Which text file do you want to use for the puzzle? ')
if not os.path.exists(filename):
    print(f'There is no file named {filename} in the working directory, giving up...')
    sys.exit()

with open(filename) as txtfile:
    txt = txtfile.read()
    txt = txt.replace('\n',' ')
    txt = txt.replace('?"','"?')
    txt = txt.replace('!"','"!')
    txt = txt.replace('."','".')
#替换正确
    txt_all = re.split('\?|\!|\.',txt)
    del(txt_all[-1])
#测试正确
#开始分割文章以及获取名字
    list_txt = txt_all
    list_name = []
	 #最好将句子根据“”分割成两个部分，可以存储在字典里面，或者二维的数组，可以尝试使用正则来得到两个部分
    length_list_txt = len(list_txt) #这个是计算有多少个句子
    list_sentence = [[None for i in range(2)]for i in range(length_list_txt)] #这里把所有的句子分为说话者和说话的内容两个部分
    for i in range(length_list_txt): 
        if '"' in list_txt[i]:
            Sentence = re.search(r"\"(.+)\"",list_txt[i])
            middle_ = list(Sentence.groups(0))#匹配在“”符号中的内容
            list_sentence[i][1]=str(middle_[0]) #将匹配到的内容给list[1],这个部分是说话的内容
  #          print(list_txt[i])
            Sentence_1 = re.search(r"\".+\"(.+)",list_txt[i])
 #           print(Sentence_1)
            Sentence_2 = re.search(r"(.+)\".+\"",list_txt[i])
  #          print(Sentence_2)
  #          print(Sentence_2.groups(0))
 #           print(Sentence_1.groups())
 #           print(len(str(Sentence_1.groups(0))))
 #           print(len(str(Sentence_2.groups(0))))
            if (Sentence_1 != None ):
                if (len(str(Sentence_1.groups(0)))>6):
 #                   print(Sentence_1.groups(0))
 #               list_sentence_analysis = list(Sentence_1.groups())
                    list_sentence[i][0] = str(Sentence_1.groups(0))
            if (Sentence_2 != None ):
                if (len(str(Sentence_2.groups(0)))>6):
  #                  print(Sentence_2.groups(0))
 #               list_sentence_analysis = list(Sentence_2.groups())
                    list_sentence[i][0] = str(Sentence_2.groups(0))
            #将剩下的部分给list[0]，这个部分是说话的人
        else:          
            list_sentence[i][0]=list_sentence[i][1] = list_txt[i] #这个部分是没有人说话的
	#开始记录统计所有人的名字，并生成对应的真值表

 #   print(list_sentence) #测试分句子是正确的
    for i in range(length_list_txt): #按照句子数量遍历
        if list_sentence[i][0]==list_sentence[i][1]: #这里是没有人说话的
  #         print(list_sentence[i][1])
            if 'Sir ' in list_sentence[i][0] :
                sentence_n = re.findall(r"Sir (\w+)",list_sentence[i][0])
                sentence_name = sentence_n
                list_name = list_name + sentence_name
            if ('Sirs ' in list_sentence[i][0] )& ('and ' in list_sentence[i][0]) :
                sentence_n = re.search(r"Sirs (.+) and (\w+)",list_sentence[i][0])
                sentence_name = str(sentence_n.groups(0)) 
                sentence_name = re.findall(r"(\w+)",sentence_name)
                list_name = list_name + sentence_name
            if ('Sirs ' in list_sentence[i][0]) & ('or ' in list_sentence[i][0]) :
                sentence_n = re.search(r"Sirs (.+) or (\w+)",list_sentence[i][0])
                sentence_name = str(sentence_n.groups(0)) 
                sentence_name = re.findall(r"(\w+)",sentence_name)
                list_name = list_name + sentence_name
        else:
            for n in range(2):
 #               print(list_sentence[i][n])
                if 'Sir ' in list_sentence[i][n] :
                    sentence_n = re.findall(r"Sir (\w+)",list_sentence[i][n])
 #                   print(sentence_n)
                    sentence_name = sentence_n
                    list_name = list_name + sentence_name
                if ('Sirs ' in list_sentence[i][n]) & ('and ' in list_sentence[i][n]) :
                    sentence_n = re.search(r"Sirs (.+) and (\w+)",list_sentence[i][n])
                    sentence_name = str(sentence_n.groups(0)) 
                    sentence_name = re.findall(r"(\w+)",sentence_name)
                    list_name = list_name + sentence_name
                if ('Sirs ' in list_sentence[i][n]) & ('or ' in list_sentence[i][n]) :
                    sentence_n = re.search(r"Sirs (.+) or (\w+)",list_sentence[i][n])
                    sentence_name = str(sentence_n.groups(0)) 
                    sentence_name = re.findall(r"(\w+)",sentence_name)
                    list_name = list_name + sentence_name
	
	#此轮循环结束之后，就得到了所有人的名字

	 #再对其中的每个元素进行分割，因为有可能有很多人因为空格连在一起
 #   print(list_name)
    length_name  = len(list_name)
    list_name_final = []
    for i in range(length_name):
        list_name_final = list_name_final +list_name[i].split()
    list_name_final = list(set(list_name_final)) #得到所有的名字，并且去重
    list_name_no_exist = ['Sir','Sirs', 'Knight','Knave','Knights','Knaves']
    list_name_final = set(list_name_final)
    list_name_no_exist = set(list_name_no_exist )
    list_name_final = list_name_final.difference(list_name_no_exist)
    list_name_final = list(list_name_final)
    list_name_final = sorted(list_name_final) #得到按照字母表顺序的列表
 #   print(list_name_final)

     
print('The Sirs are: ',end = '')
for i in range(len(list_name_final)):
    if i == len(list_name_final) - 1 :
        print(list_name_final[i],end = '')  
    else:
        print(list_name_final[i],end = ' ')   
print()
###############################################################输出姓名测试无误#####################################
###################################################################################################################
length_name_final = len(list_name_final) #同时这个也是人数对应的list，通过此表格来定位人
	#之后根据人数建立二维列表，列表的个数为2的次方的人数，列表长度为人数 ，这个也是人数
#print(length_name_final)
num_posible_list = 2**length_name_final
#print(num_posible_list)
posible_list = [[] for i in range(num_posible_list)]
for i in range(num_posible_list):
    posible_list[i] = [int(d) for d in f'{i:020b}']
    posible_list[i] = posible_list[i][-length_name_final:]
	#列出所有的可能性列表

	#开始对之前的列表进行处理，只留下说话的人和对应的句子
list_speaker_content = []
for m in range(len(list_sentence)) :
    if list_sentence[m][0] != list_sentence[m][1]:
        list_speaker_content.append(list_sentence[m])
#print(list_speaker_content)
	#这个要是成功了的话，剩下来的就是说话的人和他们说的话。
	#开始分析句子，句子其实就是判断条件，将本来的字典集合加入到里面，不符合的字典就删除，这样就好了


for sentence in list_speaker_content:
    posible_list = analyse_the_sentence(list_name_final,posible_list,sentence)
    for i in range(len(posible_list)-1,-1,-1):
        if posible_list[i]==[]:
            del posible_list[i]       
 #   print(posible_list )
		#这里就通过几轮删除把不可能的排列去掉了，剩下来的就是可能的真值表

#print(posible_list)
number_of_possible = len(posible_list)
if number_of_possible == 0 :
    print('There is no solution.')
if number_of_possible == 1 :
    print('There is a unique solution:')
    for i in range (len(list_name_final)):
        if posible_list[0][i]==1:
            print(f'Sir {list_name_final[i]:} is a Knight.')
        if posible_list[0][i]==0:
            print(f'Sir {list_name_final[i]:} is a Knave.')
if number_of_possible > 1 :
    print(f'There are {number_of_possible:} solutions.')
