#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 23:04:45 2023

@author: Killlua
"""
import multiprocessing
import os
import json
from tqdm import tqdm
from lxml import etree
from urllib import parse
import argparse
import re

parser = argparse.ArgumentParser(description='patents_analysis')
parser.add_argument('-i', '--arg1', type=str, help='input folder')
parser.add_argument('-od', '--arg2', type=str, help='output folder')
parser.add_argument('-of', '--arg3', type=str, help='output file')
args = parser.parse_args()

print('arg1:', args.arg1)
print('arg2:', args.arg2)
print('arg3:', args.arg3)

def show_files(path, all_files):
    file_list = os.listdir(path)
    for file in file_list:
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            show_files(cur_path, all_files)
        elif cur_path.endswith("html"):
            all_files.append(cur_path)
    return all_files

def export_cite(patent,arg2,arg3):
    if patent.endswith("html"):
        publn = re.search("CN.*(?=.html)", patent).group()
        with open(f'{patent}', mode='r', encoding='utf-8') as fp:
            html = fp.read()
        tree = etree.HTML(html)
        if tree is not None:
            # 提取description（这里description的内容未作任何处理）
            # description_lst = tree.xpath('//section[@itemprop="description"]//text()')
            # description = "".join(description_lst).replace('\n', "newline")
            # desc.append({'publn' : publn,
            #              'description' : description})
            # with open(f'{arg2}/{arg3}.txt', mode='a', encoding='utf-8') as fj:
            #     fj.write("{1}{0}{2}\r\n".format("|", publn, description))

            pc_elements = tree.xpath('//tr[@itemprop="backwardReferences"]')
            if pc_elements:
                for pc in pc_elements:
                    # pc_row = dict()
                    pc_html = etree.tostring(pc, pretty_print=True).decode('utf-8')
                    pc_tree = etree.HTML(pc_html)
                    # href_raw = pc_tree.xpath('//a/@href')
                    # if href_raw:
                    #     href = parse.urljoin(url, href_raw[0])
                    # else:
                    #     href = ''
                    pn = ''.join(pc_tree.xpath('//span[@itemprop="publicationNumber"]/text()')).strip()
                    # pl = ''.join(pc_tree.xpath('//span[@itemprop="primaryLanguage"]/text()')).strip()
                    ec = ''.join(pc_tree.xpath('//span[@itemprop="examinerCited"]/text()')).strip()
                    # prd = ''.join(pc_tree.xpath('//td[@itemprop="priorityDate"]/text()')).strip()
                    # pud = ''.join(pc_tree.xpath('//td[@itemprop="publicationDate"]/text()')).strip()
                    # ae = ''.join(pc_tree.xpath('//span[@itemprop="assigneeOriginal"]/text()')).strip()
                    # tl = ''.join(pc_tree.xpath('//td[@itemprop="title"]/text()')).strip()
                    # pc_row['href'] = href
                    # pn_mix = f'{pn}({pl}){ec}'
                    # pc_row['Publication number'] = pn_mix
                    # pc_row['Priority date'] = prd
                    # pc_row['Publication date'] = pud
                    # pc_row['Assignee'] = ae
                    # pc_row['Title'] = tl
                    # patent_citations.append(pc_row)
                    with open(f'{arg2}/{arg3}.txt', mode='a', encoding='utf-8') as fj:
                        fj.write("{1}{0}{2}{0}{3}\r\n".format("|", publn, pn, ec))

if __name__ == "__main__":
    # 提取文件夹内所有文件
    patents = show_files(args.arg1, [])
    print("finish listing fields")
    pool = multiprocessing.Pool(12)
    for patent in tqdm(patents, desc='patents_analysis', total=len(patents)):
        pool.apply_async(func = export_cite,args = (patent,args.arg2,args.arg3,))
    pool.close()
    pool.join()