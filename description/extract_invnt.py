#!/usr/bin/python3

import re

pattern = r"CN|ZL|中国|[0-9]{7,12}\."

with open("./google/description/grant/invnt_cite.txt","r")as f:
    for s in f.readlines():
        pnr = s.split("|")[0]
        txt = s.split("|")[1]
        if len(re.findall(pattern,txt))>0:
            with open("./google/description/grant/invnt_cite_str.txt","a")as g1:
                g1.write("{1}{0}{2}\n".format("|", pnr, txt))
        else:
            with open("./google/description/grant/invnt_ncite_str.txt","a")as g2:
                g2.write("{1}{0}{2}\n".format("|", pnr, txt))