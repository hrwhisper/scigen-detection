# -*-coding:utf-8 -*-
'''
author:  hrwhipser
功能    ： 使用knn/svm进行判别
'''

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

knn = False
realPath = './data/paper.data'
unRealPath = './data/scigen.data'
testPath = './data/test.data'
realNum = 176
unrealNum = 176

def getTestCase(path,isReal):
    test_input ,fileNames = [],[] 
    with open(path,'r') as f:
        for line in f:
            line = line.strip()
            content = line.split(' ')
            fileName = content[0]
            fileNames.append(fileName)
            temp = []
            for i in content[1:-1]:
                temp.append(float(i))
            test_input.append(temp)
    return fileNames,test_input, [isReal for i in xrange(len(test_input))]


fileNames,input1,output1 = getTestCase(realPath,True)
fileNames,input2 , output2 = getTestCase(unRealPath,False)
train_input , train_output = input1[:realNum] + input2[:unrealNum] ,output1[:realNum]+output2[:unrealNum]
fileNames,test_input , test_output = getTestCase(testPath,True)

clf = KNeighborsClassifier(n_neighbors=3) if knn else svm.SVC(gamma=0.4,C=2)
clf.fit(train_input,train_output)
predicted = clf.predict(test_input)
for filename,result in zip(fileNames,predicted):
    print filename,result