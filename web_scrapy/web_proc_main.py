#!/usr/local/bin/python3

from web_info_load_api import load_patent_info
from proc_history_manager import load_history_pts

if __name__ == '__main__':
    load_history_pts()
    load_patent_info()
    pass
