# -*-coding:utf-8 -*-
'''
author:  hrwhipser
功能    ：构建词同现网络并且计算特征，最后存入文件中
'''
import networkx as nx
import re
import os

testPaper = r'./testpaper/'
paragraphSeparator = set(['!','?','.'])
separator = re.compile(r'[!?.]')

def createGraph(fileName):
    G = nx.Graph()
    with open(fileName,'r') as f:
        curParagraph = ''
        for line in f:
            line = line.strip()
            if len(line.split(' ')) < 5: continue
            if line and line[-1] in paragraphSeparator:
                #add edge to the graph
                curParagraph = curParagraph + ' '+line
                curParagraph = separator.sub('',curParagraph)
                words = curParagraph.split(' ')
                i , lenWords = 1 , len(words)
                while i < lenWords:
                    if not words[i] and not words[i-1]:
                        del(words[i])
                        lenWords-=1
                    else:  i+=1
                    
                if lenWords >=2:
                    one , two = words[0] , words[1]
                    if one and two: G.add_edge(one,two)
                    for i in xrange(2,len(words)):
                        three = words[i]
                        if one and three: G.add_edge(one,three)
                        if two and three: G.add_edge(two,three)
                        one , two = two ,three
                #print curParagraph
                curParagraph=''
            else:
                curParagraph +=line
            
    degrees = nx.degree(G) 
    temp = sum([degrees[x] for x in degrees])
    
    try:
        node = nx.number_of_nodes(G)           #节点数
        edges= nx.number_of_edges(G)         #边数
        avgDegree =  temp / nx.number_of_nodes(G)       #平均度
        avgShort = nx.average_shortest_path_length(G)    #平均最短距离
        r = nx.diameter(G)                     #网络直径
        clu = nx.average_clustering(G)              #聚集系数
        feature = [
                    node *1.0/1849 ,                 #结点数
                    edges *1.0/12044 ,               #边数
                    avgDegree *1.0  /14  ,           #平均度
                    avgShort *1.0/3.84,              #平均最短距离
                    r *1.0/18,                       #网络直径
                    clu / 0.597602193129             #聚集系数
                ]
        return feature
    except Exception, e:
            print e

def getTestCase(path):
    saveFile = './data/test.data'
    with open(saveFile,'w') as f:
        f.write('')
    files = os.walk(path).next()[-1]
    for i , fileName in enumerate(files):
        print i , fileName
        temp_tag = False if fileName.find('scimakelatex')!=-1 else True
        feature = createGraph(path+fileName)
        if feature:
            feature = ' '.join(str(k) for k in feature) + ' ' +str(temp_tag)
            with open(saveFile,'a+') as f:
                f.write(fileName+' '+feature+'\n')

getTestCase(testPaper)