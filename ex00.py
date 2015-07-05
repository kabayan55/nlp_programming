#!/usr/bin/python
#coding: UTF-8

import sys
import string

#create a map counts
counts = {}

#open a file
#datafile = open('wiki-en-train.word','r')
datafile = open(sys.argv[1],'r')
#for each line in the file
for line in datafile:
#remove things(space, \t, \n) at the top or bottom
    line = line.strip()
#split line into words
    words = line.split()
#for w in words
    for w in words:
#if w exists in counts, add 1 to counts[w]
        if w in counts:
            counts[w] = counts[w] + 1
#else set counts[w] = 1
        else:
            counts[w] = 1
#print counts[“in”], counts[“the”] ... etc
for w in sorted(counts, key=counts.get, reverse=True):
    print(w + '\t' + str(counts[w]))


