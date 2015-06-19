# -*- coding: utf-8 -*-
'''
author:  hrwhipser
date   :  May 1, 2015
功能    ：pdf转化为txt，利用word 2013 API
'''
from win32com import client as wc 
import os
class PdfTotxt:
    def __init__(self,pdfPath,savePath):
        self.pdfPath  = pdfPath
        self.savePath = savePath
        self.word = wc.Dispatch('Word.Application') 
        # 后台运行，不显示，不警告
        self.word.Visible = 0   
        self.word.DisplayAlerts = 0
        
    def startChange(self): 
        cnt = 1
        files = os.walk(self.pdfPath ).next()[-1]
        for pdfFile in files: 
            pdfFullName = os.path.join(self.pdfPath, pdfFile) 
            dotIndex = pdfFile.rfind(".") 
            fileSuffix = pdfFile[(dotIndex + 1) : ] 
            print cnt,pdfFile
            cnt += 1
            if fileSuffix == "pdf" : 
                try:
                    doc = self.word.Documents.Open(pdfFullName) 
                    #至少两百字
                    if doc.Words.count < 200:
                        doc.Close()
                        continue
                    
                    fileName = pdfFile[ : dotIndex] +".txt" 
                    fileName = os.path.join(self.savePath, fileName) 
                    print self.pdfPath+ '\\' + pdfFile+"  ====>  " + fileName 
                    #, SaveAs method is used in versions before Word 2007. If you use Office 2010, I suggest you try Document.SaveAs2 Method.
                    #https://social.msdn.microsoft.com/Forums/en-US/a4f00910-cb6e-4861-bf96-97b0cfc6cf8f/convert-word-files-from-doc-to-docx-using-python?forum=worddev
                    doc.SaveAs2(fileName, FileFormat=2) 
                    doc.Close()
                except Exception,e:
                    print '********************ERROR',self.pdfPath+ '\\' + pdfFile,e
        self.word.Quit() 

pdfPath = r'J:\unrealpdf'
savePath = r'J:\unrealpdf\out'
task = PdfTotxt(pdfPath,savePath) 
task.startChange()
print 'ok'