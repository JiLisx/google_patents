from web_parser import PatentInfo
from proc_history_manager import is_pt_in_proc_history
import os
import requests
from lxml import etree


# Put all files which contain the publication number of patents that to be processed in one directory

def patent_info_proc(pt_tree):
    patent_info = PatentInfo()
    patent_info.load_by_data(pt_tree)
    patent_info.output_data()


def load_patent_info_file(file_path: str, load_proc):
    with open(file_path, "r") as fs:
        print("file path %s format" % file_path)
        for line in fs:
            publn = line.replace("\n", "")
            if is_pt_in_proc_history(publn):
                print("pt {} is already processed".format(publn))
                return
            else:
                url = f"https://patents.google.com/patent/{publn}"
                r = requests.get(url)
                if r.status_code == 200:
                    r.encoding = "utf-8"
                    pt_text = r.text
                    pt_tree = etree.HTML(pt_text)
                    patent_info_proc(pt_tree)
    pass


def load_patent_input(dir_path: str, load_proc):
    patent_input_path = os.path.join(os.getcwd(), dir_path)
    for dir_v in os.listdir(patent_input_path):
        dir_tmp = os.path.join(dir_path, dir_v)
        if os.path.isdir(dir_tmp):
            # for a directory, continue to traverse the directory
            load_patent_input(dir_tmp, load_proc)
        else:
            # for a file, load the file
            load_patent_info_file(dir_tmp, load_proc)
    pass
