#!/usr/bin/python
#coding: UTF-8

import sys
import string
import math

#λ1 =???,λ2 =???, V=1000000, W=0,H=0


lambda1=lambda2=float(sys.argv[1])


V = 1000000.
W = 0.
H = 0.
P1 = 0.
P2 = 0.
#create a map probabilities
from collections import defaultdict
probabilities = defaultdict(lambda: 0)
j=0
#load model into probs
modelfile = open('02-train-output.txt','r')
#for each line in model_file
for line in modelfile:
    line = line.strip()
    #split line into ngram and prob 
    words = line.split("\t")
    for ngram in words:
        if j % 2 == 0:
            w = ngram
        else:
            #P=float(words[1])
            prob = float(ngram)
            #set probabilities[w] = P
            probabilities[w] = prob
        j+=1


for foo, bar in sorted(probabilities.items()):
    print "%s --> %r" % (foo, bar)




#for each line in test_file
testfile = open('01-test-input.txt','r')


for line in testfile:
    line = line.strip()
    #split line into an array of words
    words = line.split(" ")
    #append “</s>” to the end and “<s>” to the beginning of words 
    words.append('</s>')
    words.insert(0, '<s>')
    w = words
    #for each i in 1 to length(words)-1 # 注: <s> の後に始まる
    for i in range(1, len(words)-1):
        W += 1.
        lambda1=float(sys.argv[1])
        while lambda1<1.:
            #P1 = λ1 probs[“wi”] + (1 – λ1) / V # 1-gram の平滑化された確率
            P1 = (lambda1*(probabilities[w[i]])) + ((1.-lambda1) / V)
            lambda2=float(sys.argv[1])

            while lambda2<1.:
                #P2 = λ2 probs[“wi-1 wi”] + (1 – λ2) * P1 # 2-gram の平滑化された確率 
                P2 = (lambda2*(probabilities[w[i-1]+" "+w[i]])) + ((1.-lambda2) * P1)
                #H += -log2(P2)
                H += - float(math.log(P2, 2.))
                #W += 1
                #W += 1.
                #print “entropy = ”+H/W
                print "lambda1=%0.2f, lambda2=%0.2f, entropy = %f" % (lambda1,lambda2,H/W)
                print H
                print P1
                print P2
                #print H
                lambda2+=0.2
                continue
            lambda1+=0.2
            continue
        continue
