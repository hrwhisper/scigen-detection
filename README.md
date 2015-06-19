
## 一、预处理 ##
- 将待测试的文档（txt文件）放在testpaper目录下
- 运行**txtBeautiful.py**，进行预处理

## 二、使用词同现网络判别 ##
- 运行**calFeature.py**，构建词同现网络并且计算出特征
- 运行**judge_network.py**进行判别

## 三、使用bow进行判别 ##
- 运行**judge_bow.py**进行判别即可


## 四、文件说明 ##

- calFeature.py  ： 用于词同现网络构造特征
- judge_bow.py   : bow判别
- judge_network.py ： 词同现网络判别
- printCluster.py :打印出层次聚类结果，证明bow距离度量的准确性
- scigenDownLoad.py： 用于爬取scigen论文
- trainBow.py : 计算Bow准确性
- trainKnn.py : 计算词同现网络准确性（KNN判别）
- trainSvm.py : 计算词同现网络准确性（SVM判别）
- txtBeautiful.py: txt预处理
- data : 数据文件
    - false: 伪论文（scigen生成）
    - true : 真论文
    - paper.data : 真论文词同现网络特征
    - scigen.data: 伪论文词同现网络特征
    - test.data  : 待测论文词同现网络特征
- testpaper:待测论文存放的文件夹