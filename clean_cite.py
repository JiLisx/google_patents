import os
import re
dirt = "/Users/birdstone/Dropbox/CnCitation/newdata/sipo_data1/"
os.chdir(dirt)
with open('ocr3.csv',"r") as f:
    for l in f.readlines():
        l = re.sub('\n+','',l)
        if(len(re.sub('\s','',l))>0):
            lnew = re.sub('(?<=[\u4e00-\u9fa5])\s(?=[\u4e00-\u9fa5])','',l)
            print(lnew)
            with open(dirt+"ocr3new.csv","a") as fs:
                    fs.write(lnew+'\n')

with open('ocr2.csv',"r") as f:
    for l in f.readlines():
        l = re.sub('\n+','',l)
        if(len(re.sub('\s','',l))>0):
            lnew = re.sub('(?<=[\u4e00-\u9fa5])\s(?=[\u4e00-\u9fa5])','',l)
            print(lnew)
            with open(dirt+"ocr2new.csv","a") as fs:
                fs.write(lnew+'\n')

with open('ocr1.csv',"r") as f:
    for l in f.readlines():
        l = re.sub('\n+','',l)
        if(len(re.sub('\s','',l))>0):
            lnew = re.sub('(?<=[\u4e00-\u9fa5])\s(?=[\u4e00-\u9fa5])','',l)
            print(lnew)
            with open(dirt+"ocr1new.csv","a") as fs:
                fs.write(lnew+'\n')

with open('orc10.csv',"r") as f:
    for l in f.readlines():
        l = re.sub('\n+','',l)
        if(len(re.sub('\s','',l))>0):
            lnew = re.sub('(?<=[\u4e00-\u9fa5])\s(?=[\u4e00-\u9fa5])','',l)
            print(lnew)
            with open(dirt+"ocr10new.csv","a") as fs:
                fs.write(lnew+'\n')
