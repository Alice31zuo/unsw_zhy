from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import collections
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import numpy as np
import warnings
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from  sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from collections import defaultdict

warnings.filterwarnings('ignore')

def readCsv(filename):

    data = open(filename)
    next(data)
    article_words = []
    topic = []

    for i in data:

        delNum = i.strip("\n").split('"')
        article_words.append( delNum[1] )
        topic.append( delNum[2].replace(",","") )

    data.close()

    return article_words,topic

def BagOfWords(data):
    count = CountVectorizer()
    return count.fit_transform(data)

def TfIdf(data):
    count = TfidfVectorizer()
    return count.fit_transform(data)

def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]

def getTopResult(result,clf):

    topDict = defaultdict(list)
    t = dict()

    for index, i in enumerate(result):
        topDict[i].append((index + 9501, list(clf.predict_proba(testX[index]))[0][i]))

    for key in range(0, 11):
        if key == 0:
            continue
        topList = sorted(topDict[key], key=lambda item: item[1], reverse=True)[:10]
        t[get_key(topicToNumDic, key)[0]] = [i[0] for i in topList]
    return t

if __name__ == "__main__":

    topicToNumDic = {'IRRELEVANT':0,'MONEY MARKETS':1,'BIOGRAPHIES PERSONALITIES PEOPLE':2,
              'DEFENCE':3,'ARTS CULTURE ENTERTAINMENT':4,'SCIENCE AND TECHNOLOGY':5,
              'FOREX MARKETS':6,'SPORTS':7,'SHARE LISTINGS':8,'HEALTH':9,
              'DOMESTIC MARKETS':10
              }

    trainFilename = 'training.csv'
    testFilename = 'test.csv'

    article_words,topic = readCsv(trainFilename)
    article_words2,topic2 = readCsv(testFilename)

    article_words.extend(article_words2)
    topic.extend(topic2)

    # BagOfWords
    # trainX = BagOfWords(article_words)[:9500]
    # testX = BagOfWords(article_words)[9500:]
    #
    # topicData = [topicToNumDic[i] for i in topic]
    # trainY = np.array( topicData[:9500] )
    # testY =  np.array( topicData[9500:] )

    # TfIdf
    trainX = TfIdf(article_words)[:9500]
    testX = TfIdf(article_words)[9500:]

    topicData = [topicToNumDic[i] for i in topic]
    trainY = np.array( topicData[:9500] )
    testY =  np.array( topicData[9500:] )

    #   Exploratory data analysis:
    #   1.  class distribution
    print("-" * 25, '1.1 class distribution', "-" * 25, sep='')
    sum = len(topic)

    for label,count in collections.Counter(topic).items():
        print(label, count,'{:.2%}'.format(count / sum))
        print()
    #   2.  feature statistics
    #   2.1     most frequency word
    allWord = []
    for i in article_words:
        for word in i.split(","):
            allWord.append(word)
    wordCount = collections.Counter(allWord)
    sortedWordCount = sorted( [ v for k,v in wordCount.items() ],reverse=True )
    print("-"*25,'2.1 most frequency word',"-"*25,sep='')
    print('most frequency number:',sortedWordCount[0],'')
    print('the number of occurrences:',len( get_key(wordCount,sortedWordCount[0])) )
    print('max frequency word:',get_key(wordCount,sortedWordCount[0]))

    #   2.2     least frequency word
    print("-" * 25, '2.2 least frequency word', "-" * 25, sep='')
    print('min frequency number:', sortedWordCount[-1], '')
    print('the number of occurrences:', len(get_key(wordCount, sortedWordCount[-1])))
    print('min frequency word:', get_key(wordCount, sortedWordCount[-1]))

    #   2.3     total number of words
    print("-" * 25, '2.3 total number of words', "-" * 25, sep='')
    print('Total number of words:', len( wordCount.keys() ) )

    #   2.4     most frequency topic
    topicCount = collections.Counter(topic)
    sortedTopicCount = sorted([v for k, v in topicCount.items()], reverse=True)
    print("-" * 25, '2.4 most frequency topic', "-" * 25, sep='')
    print("most frequency number:",sortedTopicCount[0])
    print('the number of occurrences:', len(get_key(topicCount, sortedTopicCount[0])))
    print('max frequency topic:', get_key(topicCount, sortedTopicCount[0]))

    #   2.5     most frequency topic except 'IRRELEVANT'
    topicCount = collections.Counter([ i for i in topic if i != 'IRRELEVANT'])
    sortedTopicCount = sorted([v for k, v in topicCount.items()], reverse=True)
    print("-" * 25, '2.5 most frequency topic except "IRRELEVANT"', "-" * 25, sep='')
    print("most frequency number:", sortedTopicCount[0])
    print('the number of occurrences:', len(get_key(topicCount, sortedTopicCount[0])))
    print('max frequency topic:', get_key(topicCount, sortedTopicCount[0]))

    #   2.6     least frequency topic
    print("-" * 25, '2.6 least frequency topic', "-" * 25, sep='')
    print('min frequency number:', sortedTopicCount[-1], '')
    print('the number of occurrences:', len(get_key(topicCount, sortedTopicCount[-1])))
    print('min frequency word:', get_key(topicCount, sortedTopicCount[-1]))

    #   3.  Models
    #       3.1 SVM

    print("-" * 25, '3.1 SVM', "-" * 25, sep='')
    clf = svm.SVC(probability=True  )
    clf.fit( trainX,trainY )
    result = clf.predict( testX )
    topDic = getTopResult(result, clf)
    for k, v in topDic.items():
        print(k)
        print(v)
        print()

    print("accuracy_score:",accuracy_score(testY, result) )
    print("precision_score_micro", precision_score(testY, result,average='micro') )
    print("recall_score_micro", recall_score(testY, result,average='micro'))
    print("precision_score_macro", precision_score(testY, result, average='macro'))
    print("recall_score_macro", recall_score(testY, result, average='macro'))
    # micro 先计算总体的TP，FN和FP的数量，再计算F1
    print("f1_score_micro:",f1_score(testY, result, average='micro'))
    # macro其实就是先计算出每个类别的F1值，然后去平均
    print("f1_score_macro:",f1_score(testY, result, average='macro'))
    print(classification_report(testY, result))

    #   3.2 MultinomialNB
    print("-" * 25, '3.2 MultinomialNB', "-" * 25, sep='')
    clf = MultinomialNB()
    clf.fit(trainX,trainY)
    result = clf.predict( testX )
    topDic = getTopResult(result,clf)
    for k,v in topDic.items():
        print(k)
        print(v)
        print()

    print("accuracy_score:",accuracy_score(testY, result) )
    print("precision_score_micro", precision_score(testY, result,average='micro') )
    print("recall_score_micro", recall_score(testY, result,average='micro'))
    print("precision_score_macro", precision_score(testY, result, average='macro'))
    print("recall_score_macro", recall_score(testY, result, average='macro'))
    # micro 先计算总体的TP，FN和FP的数量，再计算F1
    print("f1_score_micro:",f1_score(testY, result, average='micro'))
    # macro其实就是先计算出每个类别的F1值，然后去平均
    print("f1_score_macro:",f1_score(testY, result, average='macro'))
    print(classification_report(testY, result))

    print("-" * 25, '3.3 BernoulliNB', "-" * 25, sep='')
    clf = BernoulliNB()
    clf.fit(trainX, trainY)
    result = clf.predict(testX)
    topDic = getTopResult(result, clf)
    for k, v in topDic.items():
        print(k)
        print(v)
        print()
    print("accuracy_score:", accuracy_score(testY, result))
    print("precision_score_micro", precision_score(testY, result, average='micro'))
    print("recall_score_micro", recall_score(testY, result, average='micro'))
    print("precision_score_macro", precision_score(testY, result, average='macro'))
    print("recall_score_macro", recall_score(testY, result, average='macro'))
    # micro 先计算总体的TP，FN和FP的数量，再计算F1
    print("f1_score_micro:", f1_score(testY, result, average='micro'))
    # macro其实就是先计算出每个类别的F1值，然后去平均
    print("f1_score_macro:", f1_score(testY, result, average='macro'))
    print(classification_report(testY, result))

    print("-" * 25, '3.4 DecisionTreeClassifier', "-" * 25, sep='')
    clf = DecisionTreeClassifier()
    clf.fit(trainX, trainY)
    result = clf.predict(testX)
    topDic = getTopResult(result, clf)
    for k, v in topDic.items():
        print(k)
        print(v)
        print()
    print("accuracy_score:", accuracy_score(testY, result))
    print("precision_score_micro", precision_score(testY, result, average='micro'))
    print("recall_score_micro", recall_score(testY, result, average='micro'))
    print("precision_score_macro", precision_score(testY, result, average='macro'))
    print("recall_score_macro", recall_score(testY, result, average='macro'))
    # micro 先计算总体的TP，FN和FP的数量，再计算F1
    print("f1_score_micro:", f1_score(testY, result, average='micro'))
    # macro其实就是先计算出每个类别的F1值，然后去平均
    print("f1_score_macro:", f1_score(testY, result, average='macro'))
    print(classification_report(testY, result))

    print("-" * 25, '3.5 NearestNeighbors', "-" * 25, sep='')
    clf = KNeighborsClassifier()
    clf.fit(trainX, trainY)
    result = clf.predict(testX)
    topDic = getTopResult(result, clf)
    for k, v in topDic.items():
        print(k)
        print(v)
        print()

    print("accuracy_score:", accuracy_score(testY, result))
    print("precision_score_micro", precision_score(testY, result, average='micro'))
    print("recall_score_micro", recall_score(testY, result, average='micro'))
    print("precision_score_macro", precision_score(testY, result, average='macro'))
    print("recall_score_macro", recall_score(testY, result, average='macro'))
    # micro 先计算总体的TP，FN和FP的数量，再计算F1
    print("f1_score_micro:", f1_score(testY, result, average='micro'))
    # macro其实就是先计算出每个类别的F1值，然后去平均
    print("f1_score_macro:", f1_score(testY, result, average='macro'))
    print(classification_report(testY, result))

    print("-" * 25, '3.6 xgboost', "-" * 25, sep='')
    # 树的个数-10棵树建立xgboost
    # 树的深度
    # 叶子节点最小权重
    # 惩罚项中叶子结点个数前的参数
    # 所有样本建立决策树
    # 所有特征建立决策树
    # 解决样本个数不平衡的问题
    # 随机数
    clf = XGBClassifier(learning_rate=0.01,n_estimators=10,max_depth=4,min_child_weight = 1,gamma=0.,\
                      subsample=1,\
                      colsample_btree=1,\
                      scale_pos_weight=1,\
                      random_state=27,\
                      slient = 0)

    clf.fit(trainX, trainY)
    result = clf.predict(testX)
    topDic = getTopResult(result,clf)
    for k,v in topDic.items():
        print(k)
        print(v)
        print()
    print("accuracy_score:", accuracy_score(testY, result))
    print("precision_score_micro", precision_score(testY, result, average='micro'))
    print("recall_score_micro", recall_score(testY, result, average='micro'))
    print("precision_score_macro", precision_score(testY, result, average='macro'))
    print("recall_score_macro", recall_score(testY, result, average='macro'))
    # micro 先计算总体的TP，FN和FP的数量，再计算F1
    print("f1_score_micro:", f1_score(testY, result, average='micro'))
    # macro其实就是先计算出每个类别的F1值，然后去平均
    print("f1_score_macro:", f1_score(testY, result, average='macro'))
    print(classification_report(testY, result))