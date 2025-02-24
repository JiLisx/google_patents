from web_parser import PatentInfo
from proc_history_manager import is_pt_in_proc_history
import os
import requests
from common_def import HTML_DIR, INPUT_DIR
from mv_html import PatentFileOrganizer
from lxml import etree
from multiprocessing import Pool

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

def get_patent_sets(local_patents: str, input_dir: str) :
    local_set = set(patent for patent, _ in local_patents)
    diff_set = set()

    for root, _, files in os.walk(input_dir):
        for file in files:
            print("Processing files found in patent_input %s" % file)
            with open(os.path.join(root, file), "r") as f:
                for line in f:
                    patents = set(line.strip() for line in f)
                    diff_set.update(patents - local_set)

    return diff_set

def process_local_patent(pnr):
    patent, html_path = pnr
    if is_pt_in_proc_history(patent):
        print(f"Skipping processed patent {patent}")
        return
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    pt_tree = etree.HTML(html_content)
    if pt_tree is not None:
        patent_info_proc(pt_tree)
        print(f"Processed local patent {patent}")
    else:
        print(f"Error processing local file for {patent}")

def process_download_patent(patent):
    if is_pt_in_proc_history(patent):
        print(f"Skipping processed patent {patent}")
    html_content = get_patent_html(patent)
    if html_content:
        pt_tree = etree.HTML(html_content)
        if pt_tree is not None:
            patent_info_proc(pt_tree)
            print(f"Downloaded and processed patent {patent}")
    else:
        print(f"Error downloading patent {patent}")

def load_patent_info():
    local_dir = HTML_DIR
    input_dir = INPUT_DIR

    # Get local patents
    local_patents = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith(".html"):
                patent = os.path.splitext(file)[0]
                html_path = os.path.join(root, file)
                local_patents.append((patent, html_path))
                    
    # Get diff set
    diff_set = get_patent_sets(local_patents, input_dir)
    
    with Pool(2) as pool:
        
        # Process local patent
        if local_patents:
            pool.map(process_local_patent, local_patents)
        
        # Downlaod and Process 
        if diff_set:
            pool.map(process_download_patent, diff_set)