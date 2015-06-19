# -*- coding: utf-8 -*-
'''
author:  hrwhipser
功能    ：打印出聚类的结果
'''

import os
import re
from math import fabs
from PIL import Image, ImageDraw

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


    

class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def calPaperDistance(dicA, dicB):
    NA = sum([cnt for word, cnt in dicA.items()])
    NB = sum([cnt for word, cnt in dicB.items()])
    rate = NA * 1.0 / NB
    dis = 0
    for word in dicA:
        if word  in dicB: dis = dis + fabs(dicA[word] - dicB[word] * rate)
        elif (dicA[word] >> 1) != 0: dis = dis + dicA[word]
    for word in dicB:
        if word not in dicA : dis = dis + dicB[word]
    return dis * 1.0 / (NA << 1)

def hcluster(data, distance=calPaperDistance):
    distances = {}
    currentclustid = -1
    # Clusters are initially just the rows
    clust = [bicluster(name[1], id=i) for i , name in enumerate(data.items())]
    
    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)
        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                
                d = distances[(clust[i].id, clust[j].id)]
                if d < closest:  
                    closest = d
                    lowestpair = (i, j)
        # calculate the average of the two clusters
        dicA = clust[lowestpair[0]].vec
        dicB = clust[lowestpair[1]].vec
        mergevec = {}
        for word in dicA:
            if word  in dicB: mergevec[word] = (dicA[word] + dicB[word]) >> 1
            elif (dicA[word] >> 1) != 0:mergevec[word] = dicA[word] >> 1
        for word in dicB:
            if word not in dicA and (dicB[word] >> 1) != 0:
                mergevec[word] = dicB[word] >> 1
        
        # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
        right=clust[lowestpair[1]],
        distance=closest, id=currentclustid)
        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)
    return clust[0]

def printclust(clust, labels=None, n=0):
    # indent to make a hierarchy layout
    for i in range(n): print ' ',
    if clust.id < 0:
    # negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels == None: print clust.id
        else: print labels[clust.id]
    # now print the right and left branches
    if clust.left != None: printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None: printclust(clust.right, labels=labels, n=n + 1)

def getheight(clust):
    # Is this an endpoint? Then the height is just 1
    if clust.left == None and clust.right == None: return 1
    # Otherwise the height is the same of the heights of
    # each branch
    return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):
    # The distance of an endpoint is 0.0
    if clust.left == None and clust.right == None: return 0
    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance

def drawnode(draw, clust, x, y, scaling, labels,deep):
    if clust.id < 0:
        h1 = getheight(clust.left)  * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # Line length
        ll = clust.distance * scaling
        # Vertical line from this cluster to children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))
        # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))
        # Horizontal line to right item
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))
        # Call the function to draw the left and right nodes
        drawnode(draw, clust.left,  x + ll, top + h1 / 2, scaling, labels,deep+1)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels,deep+1)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id]+' '+str(deep), (0, 0, 0))

def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    # height and width
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)
    # width is fixed, so scale distances accordingly
    scaling = float(w - 150) / depth
    # Create a new image with a white background
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))
    # Draw the first node
    drawnode(draw, clust, 10, (h / 2), scaling, labels,0)
    img.save(jpeg, 'JPEG')


trainNum = 20
trueFre = calFrequent(truePath,trainNum,isTrain=True)
falseFre = calFrequent(falsePath,trainNum,isTrain=True)
train_data = dict(trueFre , **falseFre)
label = [name[0] for i , name in enumerate(train_data.items())]
root = hcluster(train_data)
printclust(root, labels=label)
drawdendrogram(root, label)

