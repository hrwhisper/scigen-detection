# -*-coding:utf-8 -*-
'''
author:  hrwhipser
功能    ：用于删除某些转化不好的文件
'''
import os
import shutil

txtPath = r'J:\realpdf\out'
files = os.walk(txtPath).next()[-1]

for file in files:
    content = None
    with open(txtPath+"\\"+file,'r') as f:
        content = f.read().lower()
    print file
    if content.find('abstract')!=-1 and content.find('references')!=-1:
        content=content[content.rfind('references'):]
        if content.find('[2]')!=-1:
            shutil.move(txtPath+'\\'+file,txtPath+'\cool\\'+file)       