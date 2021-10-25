#!/usr/bin/env python3
"""
student.py

UNSW COMP9444 Neural Networks and Deep Learning

You may modify this file however you wish, including creating
additional variables, functions, classes, etc., so long as your code
runs with the hw2main.py file unmodified, and you are only using the
approved packages.

You have been given some default values for the variables stopWords,
wordVectors(dim), trainValSplit, batchSize, epochs, and optimiser.
You are encouraged to modify these to improve the performance of your model.

The variable device may be used to refer to the CPU/GPU being used by PyTorch.

You may only use GloVe 6B word vectors as found in the torchtext package.
"""

import torch
import torch.nn as tnn
import torch.optim as toptim
from torchtext.vocab import GloVe
import numpy as np
# import sklearn

###########################################################################
### The following determines the processing of input data (review text) ###
###########################################################################

"""
type down 'python hw2main.py' in the command to run this python program

I find some tokens after tokenization are end with symbols, so I write a sample function to remove those symbols.
My stopwords is selected from the 20 most common words from vocab. However in lstm model everywords seem to be useful. 
Adding stopwords doesn't help in improving model accuracy. Therefore I remove my stopwords. 
I use regression instead of classification based on two reasons. 
Firstly, the target values are related which means it contains a enhabcement relationship between them. 
Secondly, the score function is also based on 'one star away' which means to be close also canimprove my score. 
As for the model, I use a sample 2 layers lstm with bidirectional. As for the loss function, I test MAEloss(L1loss),
MSELoss(L2loss) and smoothl1loss. I select Adma as my optimiser instead of SGD, because as for morden network Adam 
is more common use, better and faster.
I have try regression model also , when use regression model, the label need plus -1 ,and the result need return
5 class out then use argmax to choose the correct one .then plus one to get the correct label.
and the loss use CrossEntropyLoss(), and the optimizer I have try adam and Adagrad and sgd, adam performance better
than other two. but when use classification,the loss is decrease slow than the regression ,and the final
largest final score is 61.8 which is not good enough than the regression model , so I finally choose regression model.
"""


# generate n grams for tokens
# not working with lstm model
def generate_n_grams(sample, n):
    n_grams = set(zip(*[sample[i:] for i in range(n)]))
    for n_gram in n_grams:
        sample.append(' '.join(n_gram))
    return sample

def preprocessing(sample):
    """
    Called after tokenising but before numericalising.
    """
    
    # remove symbols
    for index, word in enumerate(sample):
        # find thge index of symbol
        find_index = word.find('.')
        # remove everything after symbol including symbol
        if find_index!= -1:
            word = word[:find_index]

        # same as the previous code
        find_index = word.find(',')
        if find_index!= -1:
            word = word[:find_index]

        find_index = word.find('?')
        if find_index!= -1:
            word = word[:find_index]

        find_index = word.find('!')
        if find_index!= -1:
            word = word[:find_index]

        sample[index] = word

    # generate bi_grams
    # not working, removed
    # sample = generate_n_grams(sample, 2)
        
    return sample

def postprocessing(batch, vocab):
    """
    Called after numericalisation but before vectorisation.
    """

    return batch

# I am using lstm model, it is not working with stopWords therefore I remove them
stopWords = {}

wordVectors = GloVe(name='6B', dim=100)

###########################################################################
##### The following determines the processing of label data (ratings) #####
###########################################################################

def convertLabel(datasetLabel):
    """
    Labels (product ratings) from the dataset are provided to you as
    floats, taking the values 1.0, 2.0, 3.0, 4.0, or 5.0.
    You may wish to train with these as they are, or you you may wish
    to convert them to another representation in this function.
    Consider regression vs classification.
    """

    ## Because I am using regression model, I do not need to do anything here

    return datasetLabel

def convertNetOutput(netOutput):
    """
    Your model will be assessed on the predictions it makes, which
    must be in the same format as the dataset labels.  The predictions
    must be floats, taking the values 1.0, 2.0, 3.0, 4.0, or 5.0.
    If your network outputs a different representation or any float
    values other than the five mentioned, convert the output here.
    """

    # my regression model threshold selection list
    # select first th on np.linspace(1.3, 1.7, 21), best 1.6
    # select second th on np.linspace(2.4, 2.6, 11), best 2.54
    # select third th on np.linspace(3.4, 3.6, 11), best 3.4
    # select fourth th on np.linspace(4.3, 4.7, 21), best 4.32
    # the first and fourth list are bigger becaues they two stars away from the middle 
    # which means they are more likly to get 0 score. Therefore I wanna check the with a bigger list.
    size = len(netOutput)
    # encode every netOutput in the batch
    for i in range(size):
        if netOutput[i] < 1.6:
            netOutput[i] = 1.0
        elif netOutput[i] < 2.54:
            netOutput[i] = 2.0
        elif netOutput[i] < 3.4:
            netOutput[i] = 3.0
        elif netOutput[i] < 4.32:
            netOutput[i] = 4.0
        else:
            netOutput[i] = 5.0

    return netOutput

###########################################################################
################### The following determines the model ####################
###########################################################################

class network(tnn.Module):
    """
    Class for creating the neural network.  The input to your network
    will be a batch of reviews (in word vector form).  As reviews will
    have different numbers of words in them, padding has been added to the
    end of the reviews so we can form a batch of reviews of equal length.
    """

    def __init__(self):
        super(network, self).__init__()
        # my lstm layer with 256 hidden nodes and 2 layers with bidirectional
        # the output size of it is 512
        self.lstm_layer = tnn.LSTM(100,256,2,batch_first=True,bidirectional=True,dropout=0.2)
        self.linear_layer = tnn.Linear(512,1)

    def forward(self, input, length):
        # input is [batch_size, length, ebd_dim]
        output, (h, c) = self.lstm_layer(input)
        # doing max polling though length dimension
        # I also test with average polling and use output[:,-1,:] directly, seems like max pooling has the best performance
        output = tnn.functional.max_pool2d(output, (output.shape[1], 1)).squeeze(1)
        # pred
        output = self.linear_layer(output)
        #the output size is [batch_size, 1] we need to remove the 1 dimension which is necessary before loss function
        output = output.squeeze(1)
        return output

net = network()
# perform better than l1loss and l2loss
lossFunc = tnn.SmoothL1Loss()

###########################################################################
################ The following determines training options ################
###########################################################################

# I set trainValSplit = 0.9 to have more training data
trainValSplit = 0.9
# I test 32, 64, 125, 256 and 512 batchSize, 256 batchSize has the best performance
batchSize = 256
# 25 epochs is enough
epochs = 20
# I test both adam and sgd, adam performance much better
optimiser = toptim.Adam(net.parameters(), lr=0.0006)
