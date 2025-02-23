from web_parser import PatentInfo
from proc_history_manager import is_pt_in_proc_history
import os
import requests
from common_def import HTML_DIR, INPUT_DIR
from mv_html import PatentFileOrganizer
from lxml import etree


# Put all files which contain the publication number of patents that to be processed in one directory

def patent_info_proc(pt_tree):
    patent_info = PatentInfo()
    patent_info.load_by_data(pt_tree)
    patent_info.output_data()

def get_patent_html(publn: str) -> str: 
    print(f"Downloading {publn}")
    pt_nmb = publn.replace(r".html", "")
    url = f"https://patents.google.com/patent/{pt_nmb}"
    response = requests.get(url, timeout=10)
    response.encoding = "utf-8"
    
    if response.status_code == 200 and len(response.text) > 0:
        html_content = response.text
        temp_path = os.path.join(HTML_DIR, f"{publn}.html")

        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(html_content)
       
        PatentFileOrganizer.organize_downloaded_file(publn, temp_path)
        return html_content
    else:
        print(f"Download error: {response.status_code}")
        return None

def get_patent_sets(local_dir: str, input_dir: str) :
    local_set = set()
    input_set = set()

    # Get patent in INPUT DIR
    for root, _, files in os.walk(input_dir):
        for file in files:
            print("Processing files found in patent_input %s" % file)
            with open(os.path.join(root, file), "r") as f:
                for line in f:
                    patent = line.strip()
                    input_set.add(patent)

    # Get local patent
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith(".html"):
                patent = os.path.splitext(file)[0]
                local_set.add(patent)

    diff_set = input_set - local_set
    return local_set, diff_set


def load_patent_info():
    local_dir = HTML_DIR
    input_dir = INPUT_DIR

    local_set, diff_set = get_patent_sets(local_dir, input_dir)

    # Process local patents
    for patent in local_set:
        if not is_pt_in_proc_history(patent):
            html_path = PatentFileOrganizer.locate_patent_file(patent)
            if html_path:
                with open(html_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                pt_tree = etree.HTML(html_content)
                if pt_tree is not None:
                    patent_info_proc(pt_tree)
                    print(f"Processed local patent {patent}")
                    continue
                else:
                    print(f"Could not locate HTML file for {patent}")
        else:
            print(f"Skipping processed {patent}")
    
    # Process patents that need to be download
    for patent in diff_set:
        if not is_pt_in_proc_history(patent):
            html_content = get_patent_html(patent)
            if html_content:
                pt_tree = etree.HTML(html_content)
                if pt_tree is not None:
                    patent_info_proc(pt_tree)
                    print(f"Downloaded and processed patent {patent}")
                    continue
                else:
                    print(f"Failed to download patent {patent}")
        else:
            print(f"Skipping processed {patent}")


