import argparse
import time
from search import search_single_threaded, search_multithreaded

def build_parser():
    parser= argparse.ArgumentParser(description="Multithreaded File Search Tool")
    parser.add_argument("root_dir", help="Folder to search in")
    parser.add_argument("--pattern", default="", help="Text to search for inside files")
    parser.add_argument("--content", default=None, help="Filenamepattern to search for")
    parser.add_argument("--threads", type=int, default=8, help="Number of worker threads")
    parser.add_argument("--single", action="store_true", help="Force single-threaded mode")
    return parser

def main():
    parser= build_parser()
    args= parser.parse_args()

    search_content= args.content is not None
    pattern= args.pattern if args.pattern else (args.content or "")

    start =time.time()
    if args.single:
        results= search_single_threaded(args.root_dir, pattern, search_content=search_content)
    else:
        results= search_multithreaded(args.root_dir, pattern, search_content=search_content, max_workers= args.threads)
    elapsed = time.time() - start

    for r in results:
        if r.match_type == "filename":
            print(f"[FILENAME] {r.filepath}")
        else:
            print(f"[CONTENT] {r.filepath}: {r.line_number} {r.line_preview}")

    print(f"\n{len(results)} matches found in {elapsed:.3f} seconds")

if __name__ == "__main__":
    main()