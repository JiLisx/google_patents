import os
import json
ipt_dirt = "/Volumes/WDC3/google_patents/publicationzip/"
opt_dirt = "/Volumes/WDC3/google_patents/tidydata/"
files = os.listdir(ipt_dirt)
for file in files:
    print(file)
    if file.startswith('data'):
        with open(ipt_dirt+file,"r") as f:
            for pt in f.readlines():
                patent = json.loads(pt)
                if len(patent["citation"]) > 0:
                    for cite in patent["citation"]:
                        if cite["npl_text"].__len__() == 0:
                            with open(opt_dirt+"backward.txt","a") as fs:
                                fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}\n".format("|",patent["publication_number"],
                                                                  cite["publication_number"],
                                                                  cite["application_number"],
                                                                  cite["type"],
                                                                  cite["category"]))


