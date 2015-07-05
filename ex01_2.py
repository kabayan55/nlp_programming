#!/usr/bin/python
#coding: UTF-8

import sys
import string
import math

#λ1 =0.95, λunk =1-λ1, V=1000000, W=0,H=0
#lambda1(known), lambda_unk(unknown)
lambda1 =0.95
lambda_unk = 1.0 - lambda1

#smoothing value
V = 1000000.
#test total
W = 0.
#log likelyhood
H = 0.
#unknown total
unk = 0.
#モデル読み込み
#create a map probabilities
from collections import defaultdict
probabilities = defaultdict(lambda: 0)
#probabilities = {}

i=0



#modelfile = open('01-train-answer.txt', 'r')
modelfile = open(sys.argv[1],'r')
#for each line in model_file
for line in modelfile:
    line = line.strip()
    #split line into w and P 
    words = line.split()
    for word in words:
        if i % 2 == 0:
            w = word
        else:
            #P=float(words[1])
            prob = float(word)
            #set probabilities[w] = P
            probabilities[w] = prob
        i=i+1
        
        


for foo, bar in sorted(probabilities.items()):
    print "%s --> %r" % (foo, bar)


modelfile.close()
#評価と結果表示
#testfile = open('01-test-input.txt','w')
testfile = open(sys.argv[2],'r')

#for each line in test_file
for line in testfile:
    line = line.strip() 
    #split line into an array of words
    words = line.split(" ")
    #append “</s>” to the end of words 
    words.append('</s>')
    #for each w in words
    for w in words:
        #add 1 to W
        W = W + 1.
        #setP=λunk /V
        prob = float(lambda_unk) / V
        #if probabilities[w] exists
        if w in probabilities:
            #http://docs.python.jp/2/library/sets.html
            #set P += λ1 * probabilities[w]
            prob += lambda1 * probabilities[w]
            #else
        else:
            #add 1 to unk
            unk = unk + 1.
        #add -log2 P to H
        H = H - float(math.log(prob,2.))

#print “entropy = ”+H/W
print "entropy = %f" %(H/W)
#print “coverage = ” + (W-unk)/W
print "coverage = %f" % (float(W - unk)/W)

testfile.close()

#https://github.com/Shtr28/nlp_programming_tutorial/blob/master/src/1-gram/test-unigram.py
