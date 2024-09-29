import os
import json
ipt_dirt = "/Volumes/WDC3/google_patents/publicationzip/"
opt_dirt = "/Volumes/WDC3/google_patents/tidydata/"
files = os.listdir(ipt_dirt)
#count = 0
#for file in files:
#    count += 1
#    if file == 'data000000001871':
#        print(count)
#        break
# os.chdir("/Users/birdstone/Dropbox/CnCitation/newdata/google")
# with open('sample.txt',"r") as f:
#     for pt in f.readlines():
#         patent = json.loads(pt)

for file in files:
    print(file)
    if file.startswith('data'):
        with open(ipt_dirt+file,"r") as f:
            for pt in f.readlines():
                patent = json.loads(pt)
                # if len(patent["title_localized"]) > 0:
                #     with open(opt_dirt+'title.txt','a') as fs:
                #         fs.write("{1}{0}{2}\n".format("|",patent["application_number"],
                #                                           patent["title_localized"][0]["text"]))
                # if len(patent["abstract_localized"]) > 0:
                #     with open(opt_dirt+'abstract.txt','a') as fs:
                #         fs.write("{1}{0}{2}\n".format("|",patent["application_number"],
                #                                           patent["abstract_localized"][0]["text"]))
                # if len(patent["claims_localized"]) > 0:
                #     claim = {'app_num': patent["application_number"],
                #              'claims':patent["claims_localized"][0]["text"]}
                #     with open(opt_dirt+'claims.txt','a') as fs:
                #         fs.write(json.dumps(claim)+'\n')
                # if len(patent["description_localized"]) > 0:
                #     descr = {'app_num': patent["application_number"],
                #              'descrip':patent["description_localized"][0]["text"]}
                #     with open(opt_dirt+'description.txt','a') as fs:
                #         fs.write(json.dumps(descr)+'\n')
                # # if len(patent["ipc"]) > 0:
                #     for ipc in patent["ipc"]:
                #         with open(opt_dirt + 'ipc.txt', 'a') as fs:
                #             fs.write("{1}{0}{2}\n".format("|",patent["application_number"],
                #                                           ipc["code"]))
                # with open(opt_dirt+'app_pub_number.txt','a') as fs:
                #     fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}\n".format("|", patent["publication_number"],
                #                                       patent["application_number"],
                #                                       patent["country_code"],
                #                                       patent["application_kind"],
                #                                       patent["pct_number"],
                #                                       patent["family_id"]))
                # with open(opt_dirt+'date.txt','a') as fs:
                #     fs.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}\n".format("|",patent["publication_number"],
                #                                       patent["application_number"],
                #                                       patent["publication_date"],
                #                                       patent["filing_date"],
                #                                       patent["grant_date"],
                #                                       patent["priority_date"]))
                if len(patent["citation"]) > 0:
                    for cite in patent["citation"]:
                        if cite["npl_text"].__len__() > 0:
                            with open(opt_dirt+"npc.txt","a") as fs:
                                fs.write("{1}{0}{2}{0}{3}\n".format("|",patent["publication_number"],
                                                                  cite["npl_text"],cite["category"]))
                        else:
                            with open(opt_dirt+"backward.txt","a") as fs:
                                fs.write("{1}{0}{2}{0}{3}\n".format("|",patent["publication_number"],
                                                                  cite["publication_number"],
                                                                  cite["application_number"],
                                                                  cite["type"],
                                                                  cite["category"]))

