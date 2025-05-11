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
    print(f"Requesting URL: {url}")
    
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

def get_input_patents():
    all_patents = set()
    
    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Reading input file: {file_path}")
            with open(file_path, "r") as f:
                for line in f:
                    patent = line.strip()
                    if patent:  # 非空行
                        all_patents.add(patent)
    
    return all_patents

def get_local_patents():
    local_patents = []
    
    for root, _, files in os.walk(HTML_DIR):
        for file in files:
            if file.endswith(".html"):
                patent = os.path.splitext(file)[0]
                html_path = os.path.join(root, file)
                local_patents.append((patent, html_path))
    
    return local_patents

def process_local_patent(pnr):
    patent, html_path = pnr
    encodings = ["utf-8", "latin1", "cp1252", "gbk"]
    
    for encoding in encodings:
        try:
            with open(html_path, "r", encoding=encoding) as f:
                html_content = f.read()
            pt_tree = etree.HTML(html_content)
            if pt_tree is not None:
                patent_info_proc(pt_tree)
                print(f"Processed local patent {patent}")
                return
            else:
                print(f"Error parsing HTML for {patent}")
                break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error processing {patent}: {str(e)}")
            break
    
    print(f"Failed to process {patent} with any encoding")

def process_download_patent(patent):
    html_content = get_patent_html(patent)
    if html_content:
        pt_tree = etree.HTML(html_content)
        if pt_tree is not None:
            patent_info_proc(pt_tree)
            print(f"Downloaded and processed patent {patent}")
    else:
        print(f"Error downloading patent {patent}")

'''
# This code is used to move the downloaded patent file to the target directory.
def load_patent_info():
    # Get all input patents
    all_input_patents = get_input_patents()
    print(f"Found {len(all_input_patents)} patents in input files")
    
    # Skip patents that have been processed
    patents_to_process = set()
    for patent in all_input_patents:
        if is_pt_in_proc_history(patent):
            # print(f"Skipping already processed patent: {patent}")
            pass
        else:
            patents_to_process.add(patent)
    
    print(f"After filtering history, {len(patents_to_process)} patents to process")
    
    # If no patents need to be processed, return
    if not patents_to_process:
        print("No patents need to be processed.")
        return
    
    # Get all local patents
    local_patents = get_local_patents()
    local_patent_set = {patent for patent, _ in local_patents}
    
    # Filter out local patents that need to be processed
    local_patents_to_process = []
    for patent, path in local_patents:
        if patent in patents_to_process:
            local_patents_to_process.append((patent, path))
    
    # Patents to download
    patents_to_download = list(patents_to_process - local_patent_set)
    
    print(f"Will process {len(local_patents_to_process)} local patents")
    print(f"Will download {len(patents_to_download)} patents")
    
    with Pool(2) as pool:
        # Process local patent
        if local_patents_to_process:
            pool.map(process_local_patent, local_patents_to_process)
        
        # Downlaod and Process 
        if patents_to_download:
            pool.map(process_download_patent, patents_to_download)
'''

# This code is used to re-download patent files no matter if they are already downloaded.
def load_patent_info():
    # Get all input patents
    all_input_patents = get_input_patents()
    print(f"Found {len(all_input_patents)} patents in input files")
    
    # Skip patents that have been processed
    missing_patents = set()
    for patent in all_input_patents:
        if not is_pt_in_proc_history(patent):
            missing_patents.add(patent)
    
    print(f"Found {len(missing_patents)} patents missing from processing history")
    
    # If no patents need to be processed, return  
    if not missing_patents:
        print("All patents have been processed.")
        return
    
    # Get all local patents  
    patents_to_download = list(missing_patents)
    
    print(f"Will download and process {len(patents_to_download)} patents")
    
    with Pool(2) as pool:
        # Process local patent  
        if patents_to_download:
            pool.map(process_download_patent, patents_to_download)