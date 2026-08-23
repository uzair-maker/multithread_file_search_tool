import os
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SearchResult:
    filepath: str
    match_type:str
    line_number: Optional[int]=None
    line_preview: Optional[str]= None

class SearchResultCollector:
    def __init__(self):
        self._results= []
        self._lock =threading.Lock()

    def add(self,result):
        with self._lock:
            self._results.append(result)
    
    def get_all(self):
        with self._lock:
            return list(self._results)

def collect_files(root_dir):
    all_files=[]
    for current_folder, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path= os.path.join(current_folder, filename)
            all_files.append(full_path)
    return all_files
def matches_filename_pattern(filename, pattern):
    return pattern.lower() in filename.lower()

def search_file_for_pattern(filepath,pattern):
    matches=[]
    if "__pycache__" in filepath:
        return matches
    try:
        with open(filepath,"r", encoding="utf-8", errors="ignore") as f:
            for line_number, line in enumerate(f, start=1):
                if "\x00" in line:
                    return []
                if pattern.lower() in line.lower():
                    matches.append(SearchResult(
                        filepath=filepath,
                        match_type="content",
                        line_number=line_number,
                        line_preview= line.strip()
                    ))
    except (UnicodeDecodeError, PermissionError, OSError):
        pass
    return matches

def search_single_threaded(root_dir, pattern, search_content= False):
    results=[]
    files=collect_files(root_dir)

    for filepath in files:
        filename= os.path.basename(filepath)
        if matches_filename_pattern(filename, pattern):
            results.append(SearchResult(filepath=filepath, match_type="filename"))

        if search_content:
            results.append(search_file_for_pattern(filepath, pattern))

    return results

def search_multithreaded(root_dir, pattern, search_content=False, max_workers=8):
    files= collect_files(root_dir)
    collector= SearchResultCollector()

    def process_file(filepath):
        filename = os.path.basename(filepath)
        if matches_filename_pattern(filename, pattern):
            collector.add(SearchResult(filepath=filepath, match_type="filename"))

        if search_content:
            for result in search_file_for_pattern(filepath, pattern):
                collector.add(result)
    
    with ThreadPoolExecutor(max_workers= max_workers) as executor:
        list(executor.map(process_file, files))

    return collector.get_all()

if __name__ == "__main__":
    results= search_multithreaded(".", "test", search_content=True)
    for r in results:
        print(r)