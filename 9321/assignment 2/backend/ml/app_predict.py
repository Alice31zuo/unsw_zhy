import sys
import json
import numpy as np
import joblib

# predict value according to the trained model
# data = np.array(data['data'])
# sav = joblib.load('./mel_hp.ml')
# pred = sav.predict(data.reshape(1,-1))
# result = int(round(pred[0],0))
# result_a = format(abs(result),',')
# print(result_a)
# data is given by the frontpage


def predict(data):
    data = np.array(data)
    sav = joblib.load('ml/mel_hp.ml')
    pred = sav.predict(data.reshape(1, -1))
    result = int(round(pred[0], 0)) // 1000
    result_a = format(abs(result), ',')
    return result_a
