def WAND_Algo(query_terms, top_k, inverted_index):
    list_wand = []
    for query_term in query_terms:             #set every term information as standard type
        if query_term in inverted_index:
            wand_dict = {}
            length = len(inverted_index[query_term])
            list_score, list_dic = [], []
            for i in range(length):
                list_score.append(inverted_index[query_term][i][1])
                list_dic.append(inverted_index[query_term][i][0])
            key = 'term_name'                  #record term name
            wand_dict[key] = query_term
            key = 'list_dic'                   #record relate dic
            wand_dict[key] = list_dic
            key = 'list_score'                 #record relate score
            wand_dict[key] = list_score
            key = 'max_score'                  #record max score
            wand_dict[key] = max(list_score)
            key = 'curse'                      #record current dic index
            wand_dict[key] = 0
            key = 'current_dic'                #record current dic
            wand_dict[key] = wand_dict['list_dic'][wand_dict['curse']]
            key = 'length'                     #record lenth
            wand_dict[key] = length
            list_wand.append(wand_dict)
    # this part is ok

    answer = []
    threshold = float("-inf")
    evaluation_count = 0
    dic_answer = []                           #use to record the count
    #count = top_k - 1
    while len(list_wand) != 0:
        for i in range(len(list_wand) - 1, -1, -1):       #to insure the dic is refresh and pop all dic have searched term
            if list_wand[i]['curse'] == list_wand[i]['length']:
                evaluation_count += 1
                list_wand.pop(i)
            else:
                list_wand[i]['current_dic'] = list_wand[i]['list_dic'][list_wand[i]['curse']]

        list_wand.sort(key=lambda x: x['current_dic'])    #sort the term
        score_limit = 0
        pivot = 0
        while pivot < len(list_wand):                     #set pivot
            score_limit_temp = score_limit + list_wand[pivot]['max_score']  # ???
            if score_limit_temp > threshold:
                break
            else:
                score_limit = score_limit_temp
                pivot += 1

        if len(list_wand) == 0 or pivot >= len(list_wand):    #when all term are searched , return
            return answer, len(set(dic_answer))

        if list_wand[0]['current_dic'] == list_wand[pivot]['current_dic']:    #when have target dic
            dic_answer.append(list_wand[pivot]['current_dic'])
            score = 0
            c_term = 0
            while c_term < len(list_wand) and list_wand[c_term]['current_dic'] == list_wand[pivot]['current_dic']:  #count the score
                score += list_wand[c_term]['list_score'][list_wand[c_term]['curse']]
                list_wand[c_term]['curse'] += 1
                c_term += 1
            if score > threshold:               #record the ansewer
                if len(answer) < top_k:
                    answer.append((score, list_wand[pivot]['current_dic']))
                    answer.sort(key=lambda x: (-x[0], x[1]))
                else:
                    answer.append((score, list_wand[pivot]['current_dic']))
                    answer.sort(key=lambda x: (-x[0], x[1]))
                    answer.pop(-1)
                    #count += 1
                    threshold = answer[-1][0]
        else:
            for i in range(pivot - 1, -1, -1):       #deal with the dic of term all searched
                while list_wand[i]['current_dic'] < list_wand[pivot]['current_dic']:
                    list_wand[i]['curse'] += 1
                    if list_wand[i]['curse'] == list_wand[i]['length']:
                        list_wand.pop(i)
                        pivot -= 1
                        break
                    else:
                        list_wand[i]['current_dic'] = list_wand[i]['list_dic'][list_wand[i]['curse']]
    return answer, len(set(dic_answer))















