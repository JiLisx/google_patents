import os
from common_def import FilePathDef


class ProcHistoryMgr:
    def __init__(self):
        self.proc_history_pts = set()

    def load_history_pts(self):
        if not os.path.exists(FilePathDef.PROC_HISTORY_PTS_FILE_PATH):
            return
        with open(FilePathDef.PROC_HISTORY_PTS_FILE_PATH, 'r') as fs:
            for line_str in fs:
                split_lines = line_str.split('|_')
                pt = split_lines[1].strip()
                if pt not in self.proc_history_pts:
                    self.proc_history_pts.add(pt)

    def is_pt_in_proc_history(self, pt: str):
        return pt in self.proc_history_pts

    def remove_ut(self, pt: str):
        self.proc_history_pts.remove(pt)


proc_history_mgr = ProcHistoryMgr()


def load_history_pts():
    proc_history_mgr.load_history_pts()


def is_pt_in_proc_history(pt: str):
    return proc_history_mgr.is_pt_in_proc_history(pt)


def remove_pt_history(pt: str):
    proc_history_mgr.remove_pt(pt)
