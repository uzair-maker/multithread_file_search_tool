# Multithreaded File Search Tool

A command-line file search tool built in Python that searches by filename pattern and file content, using a multithreaded thread pool for concurrent I/O. Built to demonstrate practical multithreading, thread-safe data structures, and core data structures & algorithms.

## Features

- Search files by filename pattern (case-insensitive)
- Search inside file contents, with line numbers and previews
- Multithreaded execution using a configurable thread pool
- Single-threaded mode available for comparison/benchmarking
- Automatically skips binary files and Python cache files
- Automated test suite using pytest

## Why Multithreading?

File search is I/O-bound — most time is spent waiting on disk reads, not computing. Python releases the GIL during I/O operations, so threads provide real concurrency here without the overhead of separate processes. A fixed-size thread pool (`ThreadPoolExecutor`) is used instead of spawning unbounded threads, to keep resource usage predictable on large directory trees.

## Thread Safety

Multiple worker threads write results concurrently. A `SearchResultCollector` class wraps a shared list with a `threading.Lock`, ensuring no results are lost or corrupted due to race conditions. This is verified with an automated test that runs 5 threads adding 100 results each, asserting the final count is exactly 500.

## Benchmark Results

Run on a directory with ~3,500 files (Python standard library folder):

| Mode              | Time      |
|-------------------|-----------|
| Single-threaded   | 0.573s    |
| Multithreaded (8) | 0.332s    |
| **Speedup**       | **1.73x** |

Note: on repeated runs with OS-level file caching active, the speedup advantage can shrink or disappear, since cached reads are already near-instant and thread coordination overhead outweighs the benefit. This highlights that multithreading's benefit is largest for genuine I/O-bound work, not already-cached operations.

## Project Structure
src/
search.py — core search logic (single-threaded and multithreaded)
benchmark.py — performance comparison between the two modes
cli.py — command-line interface
tests/
test_search.py — automated tests (pytest)


## Usage

```bash
# Search filenames matching "report"
python src/cli.py /path/to/folder --pattern report

# Search file contents for "TODO"
python src/cli.py /path/to/folder --content TODO

# Force single-threaded mode (for comparison)
python src/cli.py /path/to/folder --content TODO --single

# Configure thread count
python src/cli.py /path/to/folder --content TODO --threads 16
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Running the Benchmark

```bash
python src/benchmark.py
```

## Design Decisions

- **Threads over processes**: chosen because the workload is I/O-bound, not CPU-bound.
- **One task per file**: submitted to the thread pool for simple, even load distribution, rather than one task per directory.
- **Defensive file handling**: content search skips files it cannot decode as text (binary files) and skips `__pycache__` directories, to avoid false-positive matches inside compiled bytecode.