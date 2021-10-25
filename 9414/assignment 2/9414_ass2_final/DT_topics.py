# -*- coding: utf-8 -*-
import nltk
import sys
import re
import csv
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn import tree
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()
stop = stopwords.words('english')
upper_stop = [wor.capitalize() for wor in stop]


with open(sys.argv[1], "r")as csvfile :
    reader = csv.reader(csvfile,delimiter='\t',quoting = csv.QUOTE_NONE)
    rows_1 = [row for row in reader]

with open(sys.argv[2], "r")as csvfile :
    reader = csv.reader(csvfile,delimiter='\t',quoting = csv.QUOTE_NONE)
    rows_2 = [row for row in reader]

sentence_train = []
sentence_test = []
topic_result = []
id_test = []


for row in rows_1:
    sentence_train.append(row[1])
    topic_result.append(row[2])

for row in rows_2:
    id_test.append(row[0])
    sentence_test.append(row[1])

for i in range(len(sentence_train)):
    sentence_train[i] = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', ' ',sentence_train[i])
    sentence_train[i] = re.sub('[’!"&\'()*+,./:;<=>?，。?、…【】《》？“”‘’！[\\]^_`{|}~\s]+', " ", sentence_train[i])
    sen = sentence_train[i].split(' ')
    sen_1 = []
    for word in sen:
        if (word not in stop) & (word not in upper_stop):
            sen_1.append(word)
    sen_1 = [stemmer.stem(word) for word in sen_1]
    sen_1 = " ".join(sen_1)
    sentence_train[i] = sen_1

for i in range(len(sentence_test)):
    sentence_test[i] = re.sub(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', ' ',sentence_test[i] )
    sentence_test[i]  = re.sub('[’!"&\'()*+,./:;<=>?，。?、…【】《》？“”‘’！[\\]^_`{|}~\s]+', " ", sentence_test[i] )
    sen = sentence_test[i].split(' ')
    sen_1 = []
    for word in sen:
        if (word not in stop) & (word not in upper_stop):
            sen_1.append(word)
    sen_1 = [stemmer.stem(word) for word in sen_1]
    sen_1 = " ".join(sen_1)
    sentence_test[i]  = sen_1

train_data = np.array(sentence_train)
count = CountVectorizer(token_pattern=r'[A-Za-z0-9#@$%_]{2,}',lowercase= False, max_features= 200)
bag_of_words_train = count.fit_transform(train_data)
sentence_train = bag_of_words_train.toarray()
topic_result= np.array(topic_result)
sentence_test = count.transform(sentence_test).toarray()


clf = tree.DecisionTreeClassifier(criterion='entropy',random_state=0, min_samples_leaf= 20)
model = clf.fit(sentence_train, topic_result)
predicted_topic = model.predict(sentence_test)

length = len(id_test)
for i in range(length):
    print(f'{id_test[i]} {predicted_topic[i]}')


