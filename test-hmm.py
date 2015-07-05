#!/usr/bin/python
#coding: UTF-8

import sys
import string
import math
#05-train-answer.txt wiki-en-test.norm
def usage():
  print "Usage: test-hmm.py prob_file input_file"
if len(sys.argv)<3:
  usage()
  exit(0) 
N=1000000
lambda1=0.95
DEBUG1 = 0
DEBUG2 = 0
#モデル読み込み
#make a map for transition, emission, possible_tags
transition = {}
initransition = {}
emission = {}
possible_tags = []
#for each line in model_file
prob_file = open(sys.argv[1],"r")
for line in prob_file:
# split line into type, context, word, prob
    ll=line.strip()
    types,context,word,prob = ll.split(" ")
    # possible_tags[context] = 1 # 可能なタグとして保存
    if not (context in possible_tags) and (context != "<s>"):
        possible_tags.append(context)
        # 遷移確率か出現確率か読み込む
        # if type = “T”
    if types == "T":
        #  transition[“context word”] = prob
        if context == "<s>":
            initransition[word]=float(prob)
        else:    
            transition[str(context)+" "+ str(word)] = float(prob)
        # else
    else:
        #  emission[“context word”] = prob
        emission[str(context)+" "+ str(word)] = float(prob)
if DEBUG1:
    print "possible_tags:", possible_tags
    print "transition:", transition
    print "emission:", emission
prob_file.close()

input_file=open(sys.argv[2],"r")
for line in input_file:
    #前向きステップ
    #split line into words
    ll = line.strip()
    words = ll.split()
    #I = length(words)
    I = len(words)
    if DEBUG2:
        print words
    #make maps best_score, best_edge
    best_score = {}
    best_edge = {}
    #best_score[“0 <s>”] = 0 # <s> から始まる。0はもじれつになってる
    best_score[str(0)+" "+"<s>"] = 0
    #best_edge[“0 <s>”] = {}
    best_edge[str(0)+" "+ "<s>"] = {}

    #possible_tags から <s> を省くと，先頭が例外処理となる
    #ここでは prev のループは不要で i=0 に決め打ちなので表現を具体化した
    #先に i=1,2,...,I-1 のmain loopを読んでからこの例外処理を読むと理解しやすい
    #prev="<s>"; i=0  # 覚え書き
    for next1 in possible_tags: # next は予約語なので使えない
        # 以下 best_score=0 に -log PT(next|"<s>") を加える
        if next1 in initransition:
            score = best_score[str(0)+" "+ "<s>"] -math.log(initransition[next1])
            # nxt+" <s>" は emission に含まれないので，これでおしまい
            if lambda1!=1.0:  # 未知語の確率処理
                score=score-math.log((1-lambda1)/N) 
            else:
                score=10**10 # -log 0 の代わり
            if not ("1 "+next1 in best_score) or (best_score["1 "+next1] > score):
                best_score["1 "+next1] = score
                best_edge["1 "+next1] = "0 <s>"




    #for i in 0 ... I-1:
    for i in range(1,I):
        # for each prev in keys of possible_tags
        for prev in possible_tags:
            #  for each next in keys of possible_tags
            for next1 in possible_tags:
                #   if best_score[“i prev”] and transition[“prev next”] exist #iはint
                if (str(i)+" "+ prev in best_score) and (prev+" "+ next1 in transition):
                    #    score = best_score[“i prev”] -log PT(next|prev) + -log PE(word[i]|next) #nextは予約語
                    score = best_score[str(i)+" "+ prev] -math.log(float(transition[prev+" "+next1]))
                     #    if best_score[“i+1 next”] is new or > score
                    if next1+" "+words[i] in emission:
                        score = score-math.log(lambda1*float(emission[next1+" "+words[i]])+(1-lambda1)/N) 
                    elif lambda1!=1.0: #未知語の確率処理
                        score=score-math.log((1-lambda1)/N)
                    else:
                        score = 10*10
                    if not (str(i+1)+" "+next1 in best_score) or (best_score[str(i+1)+" "+next1] > score):

                        #     best_score[“i+1 next”] = score
                        best_score[str(i+1)+" "+ next1] = score
                        #     best_edge[“i+1 next”] = “i prev”
                        best_edge[str(i+1)+" "+ next1] = str(i)+" "+ prev
    # 最後、</s>に対して同じ操作を行う
    for prev in possible_tags: # 今回は next は </s> で品詞タグは無く決め打ち
        # 直前の best_score に -log PT(</s>|prev) のみ加える
        if (str(I)+" "+prev in best_score) and (prev+" "+"</s>" in transition):
            score = best_score[str(I)+" "+prev] -math.log(float(transition[prev+" "+"</s>"]))
            if ((not (str(I+1)+" "+"</s>" in best_score)) or (best_score[str(I+1)+" "+"</s>"] > score)):
                best_score[str(I+1)+" "+"</s>"] = score
                best_edge[str(I+1)+" "+"</s>"] = str(I)+" "+prev

    #後ろ向きステップ
    #tags = [ ]
    tags = [ ]
    #next_edge = best_edge[ “I </s>” ]
    next_edge = best_edge[str(I+1)+ " " + "</s>"]
    #while next_edge != “0 <s>”
    while next_edge != str(0)+" "+ "<s>":
        # このエッジの品詞を出力に追加
        # split next_edge into position, tag
        position, thistag = next_edge.split(" ")
        # append tag to tags
        tags.append(thistag)
        # next_edge = best_edge[ next_edge ]
        next_edge = best_edge[ next_edge ]
    #tags.reverse()
    tags.reverse()
    #join tags into a string and print
    tagstr=" ".join(tags)
    print tagstr
input_file.close()
