#!/usr/bin/python
#coding: UTF-8

import sys
import string
import math



modelfile = open('titles-en-train.labeled','r')

for line in modelfile:
    line = line.strip()
    words = line.split("\t")

#1つの事例に対する予測
#predict_one(w, phi)
def predict_one(w, phi):
    #score = 0
    score = 0
    #for each name, value in phi
    for name, value in sorted(phi.value()):
        #if name exists in w
        if name in w:
            #score += value * w[name]
            score += value * w[name]
            #if score >= 0 return 1
            if score >= 0:
                return 1
                #else
            else:
                #return -1
                return -1
            
    #素性作成（1-gram素性）    
#CREATE_FEATURES(x):
def create_features(x):
#create map phi 
    from collections import defaultdict
    phi = defaultdict(lambda: 0)
    #split x into words
    x = x.strip
    words = x.split("\t")
    #for word in words
    for word in words:
        # 「 UNI: 」を追加して 1-gram を表す
        #phi[“UNI:”+word] += 1
        phi.insert(0, "UNI:")
        phi += 1
        #return phi
        return phi
    

#update_weights(w, phi, y)
def update_weights(w, phi, y):
    #for name, value in phi:
    for name, value in phi:
        #w[name] += value*y
        w[name] += value * y




#create map w
w = {}
#for I iterations（くりかえし）10くらいが一番いい
#wはおもみ
for I in range(I):
    
    #for each labeled pair x, y in the data 
    #ここが一行読み取り？
    for x, y in data: 
        #phi = create_features(x)
        phi = create_features(x)
        #y' = predict_one(w, phi) 
        y2 = predict_one(w,phi)
        
        #if y' != y
        if y2 != y:
            #update_weights(w, phi, y)
            update_weights(w, phi, y)




#for l in labelled_data.seek(0)







