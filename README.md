# CS172 Part A – Web Crawler

## Overview

This project implements a Scrapy-based web crawler that collects public technical documentation pages related to:

* Artificial Intelligence
* Machine Learning
* Python programming
* Data science libraries

The crawler reads seed URLs from a file, follows links within approved domains, stores raw HTML pages, and generates metadata for future indexing and search.

---

## Features

* Reads seed URLs from `seed_urls.txt`
* Crawls HTML pages using Scrapy
* Saves raw HTML files locally
* Generates metadata in JSONL format
* Supports configurable crawl size
* Supports configurable crawl depth
* Handles duplicate URLs automatically

---

## Requirements

* Python 3.10+
* pip

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How To Run

Move into outer crawler directory:

```bash
cd webcrawler
```

Run crawler:

```bash
scrapy crawl html_spider -a output_dir=raw_html -s CLOSESPIDER_PAGECOUNT=1000
```

---

## Parameters

### Output Directory

`output_dir` defines where crawled HTML files are saved.

Example:

```bash
scrapy crawl html_spider -a output_dir=mycrawl
```

### Page Count

`CLOSESPIDER_PAGECOUNT` defines the maximum number of pages to crawl.

Example:

```bash
scrapy crawl html_spider -a output_dir=raw_html -s CLOSESPIDER_PAGECOUNT=500
```

---

## Seed URLs

Seed URLs are stored in:

```txt
webcrawler/seed_urls.txt
```

---

## Output

After running, the crawler creates:

```txt
raw_html/
```

Contents:

```txt
raw_html/
    *.html
    metadata.jsonl
```

* `.html` files contain raw webpage HTML
* `metadata.jsonl` stores page metadata

Example metadata entry:

```json
{
  "url": "https://docs.python.org/3/tutorial/",
  "title": "Python Tutorial",
  "file_path": "raw_html/000001.html",
  "content_type": "text/html",
  "status": 200
}
```

---

## Notes

* Duplicate URLs are handled automatically by Scrapy
* Crawl depth is controlled by `DEPTH_LIMIT`
* `raw_html/` is excluded from GitHub using `.gitignore`
* Designed for the CS172 Information Retrieval project
