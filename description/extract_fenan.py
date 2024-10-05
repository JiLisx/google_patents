#!/usr/bin/python3

import re

pattern = "(?<=newline)[^newline]*分案申请[^newline]*(?=newline)"

with open("desc_fenan.txt","r")as f:
    for s in f.readlines():
        pnr = s.split("|")[0]
        txt = s.split("|")[1]
        for c in re.findall(pattern, txt):
            for cite in re.findall("[0-9]{7,}",c):
                print(cite)
                with open("fenan_cite.txt","a")as g:
                    g.write("{1}{0}{2}\n".format("|", pnr, cite))