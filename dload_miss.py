#!/usr/local/bin/python3
import requests
import os
path = "/Volumes/WDC5/google_patents/description"
os.chdir(path)

with open("finish_missing.txt", 'r') as file:
    finish = [line.strip() for line in file.readlines()]

with open("missing.txt","r") as f:
    for pt in f.readlines():
        pt = pt.strip().replace("./","/")
        if pt not in finish:
            pt_nmb = pt.split("/")[4].replace(r".html","")
            url = "https://patents.google.com/patent/" + pt_nmb
            r = requests.get(url)
            r.encoding = "utf-8"
            if len(r.text) > 0:
                with open(path+pt,"w") as fs:
                    print(path+pt)
                    #print(r.text)
                    fs.write(r.text)
                with open("finish_missing.txt","a") as g:
                    g.write(pt+"\n")
