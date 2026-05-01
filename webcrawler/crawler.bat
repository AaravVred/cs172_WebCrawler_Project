@echo off
REM Usage: crawler.bat <output-dir> <page-count>
REM Example: crawler.bat raw_html 1000

set OUTPUT_DIR=%1
set PAGE_COUNT=%2

if "%OUTPUT_DIR%"=="" set OUTPUT_DIR=raw_html
if "%PAGE_COUNT%"=="" set PAGE_COUNT=1000

scrapy crawl html_spider -a output_dir=%OUTPUT_DIR% -s CLOSESPIDER_PAGECOUNT=%PAGE_COUNT%