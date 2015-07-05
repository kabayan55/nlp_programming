#!/usr/bin/python
#coding: UTF-8

import sys
import string

#create map counts, context_counts
#2つの単語の連なりの数を数えるのに使ってる
counts = {}
context_counts = {}
trainingfile = open('02-train-input.txt','r')
#trainingfile = open('wiki-en-train.word','r')
#trainingfile = open(sys.argv[1],'r')
#for each line in the training_file
for line in trainingfile:
    line = line.strip()
    #split line into an array of words
    words = line.split(" ")
    #append “</s>” to the end and “<s>” to the beginning of words 
    words.append('</s>')
    words.insert(0, '<s>')
    w=words
    #for each i in 1 to length(words)-1 # 注: <s> の後に始まる
    for i in range(1,len(words)-1):
        #2-gram
        if w[i-1] + " " + w[i] in counts:
            counts[w[i-1]+ " " + w[i]] += 1 
            if w[i-1] in context_counts:
                context_counts[w[i-1]] += 1
            else:
                context_counts[w[i-1]] = 1
        else:
            counts[w[i-1]+ " " + w[i]] = 1
            if w[i-1] in context_counts:
                context_counts[w[i-1]] += 1
            else:
                context_counts[w[i-1]] = 1
                

                    #1-gram
        if w[i] in counts:
            counts[w[i]]+=1
            if "" in context_counts:
                context_counts[""]+=1
            else:
                context_counts[""]=1
        else:
            counts[w[i]]=1
            if "" in context_counts:
                context_counts[""]+=1
            else:
                context_counts[""]=1
         

print counts
print words                
   
#open the model_file for writing 
modelfile = open('02-train-output.txt','w')
#modelfile = open(sys.argv[2],'w')
#for each ngram, count in counts
for ngram, count in sorted(counts.items()):
    #split ngram into an array of words 
    words = ngram.split(" ")
    #remove the last element of words
    words.pop()
    #join words into context
    context = "".join(words)
    # “wi-1 wi” → {“wi-1”, “wi”} # {“wi-1”, “wi”} → {“wi-1”} # {“wi-1”} → “wi-1”
    #probability = counts[ngram]/context_counts[context] 
    #print counts
    #print context_counts
    probability = float(counts[ngram])/context_counts[context]
    #print ngram, probability to model_file
    modelfile.write("{0:s}\t{1:f}\n".format(ngram, probability))
    print "%s\t%r" % (ngram, probability)

