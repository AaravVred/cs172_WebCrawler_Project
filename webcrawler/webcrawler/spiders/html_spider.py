import os
import hashlib
from urllib.parse import urlparse

import scrapy
import json

class HtmlSpider(scrapy.Spider):
    name = "html_spider"

    custom_settings = {
        "ROBOTSTXT_OBEY": True,         # for robots.txt on websites
        "CONCURRENT_REQUESTS": 16,      
        "DOWNLOAD_DELAY": 0.25,
        "DEPTH_LIMIT": 3,               # max link hops from seed urls
        "CLOSESPIDER_PAGECOUNT": 1000,  # max pages to crawl (can override)
        "HTTPCACHE_ENABLED": False,     # no caching so fresh pages can be downloaded
        "LOG_LEVEL": "INFO",
    }

    start_urls = []

    with open("seed_urls.txt", "r") as f:
        start_urls = [line.strip() for line in f if line.strip()]

    allowed_domains = [             # restricts crawling to these domains only
        "docs.python.org",
        "flask.palletsprojects.com",
        "docs.djangoproject.com",
        "scikit-learn.org",
        "pandas.pydata.org",
        "numpy.org",
        "www.elastic.co",
        "lucene.apache.org",
    ]

    def __init__(self, output_dir="raw_html", *args, **kwargs):     
        super().__init__(*args, **kwargs)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.saved_count = 0

    def parse(self, response):      
        content_type = response.headers.get("Content-Type", b"").decode("utf-8").lower()

        if "text/html" not in content_type:     # skip non-html pages
            return

        url_hash = hashlib.sha256(response.url.encode("utf-8")).hexdigest()  # unique hashes to prevent filename collisions
        parsed = urlparse(response.url)
        domain = parsed.netloc.replace(":", "_")
        filename = f"{self.saved_count:06d}_{domain}_{url_hash}.html"   # unique filename
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "wb") as f:     # save raw html
            f.write(response.body)

        json_path = os.path.join(self.output_dir, "metadata.jsonl")

        record = {      # metadata record for current page
            "url": response.url,
            "title": response.css("title::text").get(),
            "file_path": filepath,
            "content_type": content_type,
            "status": response.status
        }

        with open(json_path, "a", encoding="utf-8") as jf:  # append metadata as one json line
            jf.write(json.dumps(record) + "\n")

        self.saved_count += 1       # increment saved file counter

        for link in response.css("a::attr(href)").getall():     # get all links
            if link.startswith(("mailto:", "tel:", "javascript:", "#")):
                continue
            yield response.follow(link, callback=self.parse)    # follow valid links recursively