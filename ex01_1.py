#!/usr/bin/python
#coding: UTF-8

import sys
import string

#create a map counts
counts = {}

#create a variable total_count = 0
total_count = 0

#trainingfile = open('01-train-input.txt','r')
trainingfile = open(sys.argv[1],'r')
#for each line in the training_file 
for line in trainingfile:
    line = line.strip()    
    #split line into an array of words 
    words = line.split(" ")
    #append “</s>” to the end of words
    words.append('</s>')
    # for each word in words
    for word in words:
        #add 1 to counts[word] 
        #add 1 to total_count
        if word in counts:
            counts[word] = counts[word] + 1
            total_count = total_count + 1
        else:
            counts[word] = 1
            #total count increases every time, so add 1
            total_count += 1
        
#open the model_file for writing 
#modelfile = open('01-train-model.txt', 'r')
modelfile = open(sys.argv[2],'w')
#for each word, count in counts
for word in sorted(counts):
    #probability = counts[word]/total_count
    probability = float(counts[word])/float(total_count)
    #print word, probability to model_file
    modelfile.write("%s\t%f\n" %(word,probability))
modelfile.close()

#モデルファイルをつくってる！
