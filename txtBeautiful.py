# -*-coding:utf-8 -*-
'''
author:  hrwhipser
功能    :  对pdf转化成的txt进行预处理，如删除作者信息
'''
import re
import os
refer = re.compile(r'\[\d*\]')
other = re.compile(r'[(),<>-_"]')
num = re.compile(r'\d+(.\d+)?')
txtpath = r'./testpaper/'
outpath = r'./testpaper/'

files = os.walk(txtpath).next()[-1]
for file in files:
    print file
    with open(txtpath+file,'r') as f:
        content = f.read().lower()
        #去除作者信息
        temp_index = content.find('abstract') 
        if temp_index != -1: content = content[temp_index+8:]
        #去除参考文献信息
        temp_index = content.rfind('references')    
        if temp_index != -1: content = content[:temp_index]
        f.close()
        with open(outpath+file, 'w') as wf:   
            wf.write(num.sub('1',other.sub(' ',refer.sub('',content))))