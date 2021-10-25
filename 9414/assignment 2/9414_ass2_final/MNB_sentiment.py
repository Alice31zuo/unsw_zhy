# -*- coding: utf-8 -*-
import nltk
import sys
import re
import csv
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn import tree
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# get the stopwords list
stemmer = PorterStemmer()
stop = stopwords.words('english')
upper_stop = [wor.capitalize() for wor in stop]

#open file and get the constent
with open(sys.argv[1],"r")as csvfile:
    reader=csv.reader(csvfile,delimiter='\t',quoting=csv.QUOTE_NONE)
    rows_1=[row for row in reader]

with open(sys.argv[2],"r")as csvfile:
    reader=csv.reader(csvfile,delimiter='\t',quoting=csv.QUOTE_NONE)
    rows_2=[row for row in reader]


sentence_train = []
sentence_test = []
sentiment_result = []
id_test = []

for row in rows_1:
    sentence_train.append(row[1])
    if 'negative' in row[3] :
        sentiment_result.append('negative')
    elif 'neutral' in row[3] :
        sentiment_result.append('neutral')
    else :
        sentiment_result.append('positive')

for row in rows_2:
    id_test.append(row[0])
    sentence_test.append(row[1])

#deal with the sentence :delete the stopwords and get the stem words
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

#get the feature words and create the senteces array
train_data = np.array(sentence_train)
count = CountVectorizer(token_pattern=r'[A-Za-z0-9#@$%_]{2,}',lowercase= False)
bag_of_words_train = count.fit_transform(train_data)
sentence_train = bag_of_words_train.toarray()
sentiment_result = np.array(sentiment_result)
sentence_test = count.transform(sentence_test).toarray()

#start to train and predict
clf = MultinomialNB(alpha=1 ,class_prior= None,fit_prior= True)
model = clf.fit(sentence_train, sentiment_result)
predicted_sentiment = model.predict(sentence_test)

length = len(id_test)
for i in range(length):
    print(f'{id_test[i]} {predicted_sentiment[i]}')

