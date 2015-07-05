#!/usr/bin/python
#coding: UTF-8

import sys
import string

def usage():
    print "Usage:python train-hmm.py model_file"

if len(sys.argv)<2:
    usage()
    exit(0)


# 入力データ形式は「 natural_JJ language_NN ... 」 
#make a map emit, transition, context
emit={}
transition={}
context={}
context["<s>"]=0

#wiki-en-train.norm_pos
file = open(sys.argv[1],"r")
#for each line in file
for line in file:
    line=line.strip()
    # previous = “<s>”
    previous = "<s>"
    # context[previous]++
    context[previous]+=1
    # split line into wordtags with “ “
    ll = line.split(" ")
    # for each wordtag in wordtags
    for wordtags in ll:
        # 文頭記号
        #  split wordtag into word, tag with “_” 
        word,tag = wordtags.split("_")
        #  transition[previous+“ “+tag]++ # 遷移を数え上げる
        if previous+" "+tag in transition:
            transition[previous + " " + tag] += 1
        else:
            transition[previous + " " + tag] = 1
        #  context[tag]++
        if tag in context:
            context[tag]+=1
        else:
            context[tag]=1
        #  emit[tag+“ “+word]++
        if tag+" "+word in emit:
            emit[tag + " " + word]+=1
        else:
            emit[tag + " " + word]=1
        #  previous = tag
        previous = tag
        # transition[previous+” </s>”]++ 
        transition[previous+" "+"</s>"]=1 
# 遷移確率を出力
#for each key, value in transition
for key in transition:
    # 文脈を数え上げる # 生成を数え上げる
    # split key into previous, word with “ “
    prev, word = key.split(" ")
    # print “T”, key, value/context[previous]
    print "T", key, float(transition[key])/context[prev]
# 同じく生成確率を出力(「T」ではなく「E」を付与)
for key in emit:
    prev, word = key.split(" ")
    print "E", key, float(emit[key])/context[prev]

