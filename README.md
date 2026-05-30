# CS172 Information Retrieval Project

## Overview

This project implements:

1. A Scrapy-based web crawler (Part A)
2. A PyLucene search engine and Flask web interface (Part B)

The crawler collects technical documentation pages and stores raw HTML files. The search engine indexes the collected pages and returns ranked search results using Lucene.

---

## Requirements

Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
pip install beautifulsoup4 flask
```

PyLucene must also be installed.

---

# Part A - Web Crawler

Run crawler:

```bash
cd webcrawler

scrapy crawl html_spider \
-a output_dir=raw_html_dataset \
-s CLOSESPIDER_PAGECOUNT=1000
```

Output:

```txt
raw_html_dataset/
    *.html
    metadata.jsonl
```

---

# Part B - Build Index

Build the Lucene index:

```bash
cd webcrawler

python3 indexer.py
```

Example output:

```txt
Indexed 7270 documents into lucene_index
```

This creates:

```txt
lucene_index/
```

---

# Part B - Command Line Search

Run:

```bash
python3 search.py
```

Example:

```txt
Enter search query: machine learning
```

The system returns:

* Lucene score
* Page title
* Original URL
* Local file path

---

# Part B - Web Search Interface

Start the Flask application:

```bash
python3 app.py
```

Server:

```txt
http://127.0.0.1:8888
```

If running through the CS172 server, create an SSH tunnel, or open a new local terminal and run:

```bash
ssh -L 8899:class-043.cs.ucr.edu:8888 <netid>@bolt.cs.ucr.edu
```

Then open this in a browser like chrome:

```txt
http://127.0.0.1:8899
```

The interface provides:

* Search textbox
* Search button
* Top 10 ranked results
* Lucene scores
* Original URLs
* Local file paths

---

## Files

```txt
indexer.py            Build Lucene index
search.py             Command-line search
app.py                Flask web application
templates/index.html  Search interface
```

---

## Notes

* Dataset directory: `raw_html_dataset/`
* Lucene index directory: `lucene_index/`
* Results are ranked using Lucene relevance scoring.
* Raw datasets are excluded from GitHub because of size.