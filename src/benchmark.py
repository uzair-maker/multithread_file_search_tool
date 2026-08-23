import time
from search import search_single_threaded, search_multithreaded

def run_benchmark(root_dir, pattern):
    print("Running single_threaded search...")
    start= time.time()
    single_results= search_single_threaded(root_dir, pattern, search_content=False)
    single_time= time.time()- start
    print(f"Single-threaded:{len(single_results)}matches in {single_time:.3f} seconds")
    
    print("Running multithreaded search...")
    start = time.time()
    multi_results= search_multithreaded(root_dir, pattern, search_content=False,max_workers=8)
    multi_time= time.time() -start
    print(f"Multithreaded: {len(multi_results)} matches in {multi_time:.3f} seconds")

    speedup = single_time/multi_time
    print(f"\nSpeedup: {speedup:.2f}x faster with threading")

if __name__ == "__main__":
    root = r"C:\Users\SABRI LAPTOP\AppData\Local\Python\pythoncore-3.14-64"
    run_benchmark(root,"test")