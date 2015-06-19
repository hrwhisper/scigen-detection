# -*-coding:utf-8 -*-

from sklearn import svm,metrics


realPath = './data/paper.data'
unRealPath = './data/scigen.data'
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
    return test_input, [isReal for i in xrange(len(test_input))]


input1,output1 = getTestCase(realPath,True)
input2 , output2 = getTestCase(unRealPath,False)
train_input , train_output = input1[:realNum] + input2[:unrealNum] ,output1[:realNum]+output2[:unrealNum]
test_input , test_output = input1[realNum:] + input2[unrealNum:] ,output1[realNum:]+output2[unrealNum:]

clf = svm.SVC(gamma=0.4,C=2)
clf.fit(train_input,train_output)
predicted = clf.predict(test_input)
print predicted
print("Classification report for classifier %s:\n%s\n" % (clf, metrics.classification_report(test_output, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(test_output, predicted))