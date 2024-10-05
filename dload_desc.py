#!/usr/local/bin/python3
import requests
import os
from lxml import etree
import multiprocessing

def dl_pt(pt):
    url = "https://patents.google.com/patent/" + pt
    r = requests.get(url)
    r.encoding = "utf-8"
    return r.text

def export_desc(pt,pt_text,path):
    tree = etree.HTML(pt_text)
    if tree is not None:
        description_lst = tree.xpath('//section[@itemprop="description"]//text()')
        description = "".join(description_lst).replace('\n', "newline")
        with open(path+ 'desc_23.txt', mode='a', encoding='utf-8') as fj:
            fj.write("{1}{0}{2}\r\n".format("|", pt, description))

# def export_cite(pt,pt_text,path):
#     tree = etree.HTML(pt_text)
#     if tree is not None:
#         pc_elements = tree.xpath('//tr[@itemprop="backwardReferences"]')
#         if pc_elements:
#             for pc in pc_elements:
#                 pc_html = etree.tostring(pc, pretty_print=True).decode('utf-8')
#                 pc_tree = etree.HTML(pc_html)
#                 pn = ''.join(pc_tree.xpath('//span[@itemprop="publicationNumber"]/text()')).strip()
#                 ec = ''.join(pc_tree.xpath('//span[@itemprop="examinerCited"]/text()')).strip()
#                 with open(path+ 'grant_cite.txt', mode='a', encoding='utf-8') as fj:
#                     fj.write("{1}{0}{2}{0}{3}\r\n".format("|", pt, pn, ec))

def d_parse(pt,path):
    pt_text = dl_pt(pt)
    export_desc(pt, pt_text, path)
    # export_cite(pt, pt_text, path)
    with open(path + "finish.txt", "a") as g:
        g.write(pt + "\n")

if __name__ == "__main__":
    path = "/Volumes/WDC5/google_patents/"
    os.chdir(path)
    with open("finish.txt", 'r') as file:
        finish = [line.strip() for line in file.readlines()]
    with open("cnpinfo1_2023.txt","r") as f:
        pts = [line.replace("\n","") for line in f.readlines()]
    pool = multiprocessing.Pool(12)
    for pt in pts:
        if pt not in finish:
            pool.apply_async(func=d_parse, args=(pt, path, ))
    pool.close()
    pool.join()