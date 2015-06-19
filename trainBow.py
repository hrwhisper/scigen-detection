# -*-coding:utf-8 -*-
'''
author:  hrwhipser
功能    ： 测试bag of words精度
'''

import os
import re
from math import fabs

truePath = r'./data/true'
falsePath = r'./data/false'
separator = re.compile(r'[!?.\n\t\r]')

def calFrequent(path,num,isTrain=True):
    frequencies = {}
    files = os.walk(path).next()[-1][:num] if isTrain else os.walk(path).next()[-1][num:] 
    for fileName in files:
        content = ''
        with open(path + '/' + fileName, 'r') as f:
            content = f.read()
        content = separator.sub(' ', content)
        words = content.split(' ')
        curDic = {}
        for word in words:
            if word:
                curDic.setdefault(word, 0)
                curDic[word] += 1
                
        frequencies[fileName] = curDic
    # dic{ filename dic{word:wordCnt} }
    return frequencies


def calPaperDistance(dicA, dicB):
    NA = sum([cnt for word, cnt in dicA.items()])
    NB = sum([cnt for word, cnt in dicB.items()])
    #if NA==0 or NB==0:return 0x7ffffff
    rate = NA * 1.0 / NB
    dis = 0
    for word in dicA:
        if word  in dicB: dis = dis + fabs(dicA[word] - dicB[word] * rate)
        elif (dicA[word] >> 1) != 0: dis = dis + dicA[word]
    for word in dicB:
        if word not in dicA : dis = dis + dicB[word]
    return dis * 1.0 / (NA << 1)


trainNum = 176
trueFre = calFrequent(truePath,trainNum,isTrain=True)
falseFre = calFrequent(falsePath,trainNum,isTrain=True)
train_data = dict(trueFre , **falseFre)
train_fileName = [name[0] for i , name in enumerate(train_data.items())]

trueFre = calFrequent(truePath,trainNum,isTrain=False)
falseFre = calFrequent(falsePath,trainNum,isTrain=False)
test_data = dict(trueFre , **falseFre)
test_fileName = [name[0] for i , name in enumerate(train_data.items())]

rightNum_real = rightNum_noReal = 0
real_num = noReal_num = 0

k = 3

for fileName , wordCnt in test_data.items():
    tag = False if fileName.find('scimakelatex')!=-1 else True
    if tag: real_num += 1
    else: noReal_num += 1
    distances  = [(fileTrain,calPaperDistance(wordCnt, wordCntTrain)) for  fileTrain,wordCntTrain in train_data.items()]
    distances.sort(key=lambda x:x[1])
    truePaper = falsePaper = 0
    for name , dis in distances[:k]:
        temp_tag = False if name.find('scimakelatex')!=-1 else True
        if temp_tag: truePaper+=1
        else: falsePaper+=1
    if truePaper > falsePaper and tag: rightNum_real +=1
    elif truePaper < falsePaper and not tag:rightNum_noReal+=1

print '正样本（真论文总数）',real_num
print '负样本（假论文总数）', noReal_num  
print '判断为正样本且正确的个数',rightNum_real 
print '判断为负样本且正确的个数',rightNum_noReal
print rightNum_real+rightNum_noReal,len(test_data),(rightNum_real+rightNum_noReal) *1.0/len(test_data)