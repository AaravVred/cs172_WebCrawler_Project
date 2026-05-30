import os
import json
import shutil
from bs4 import BeautifulSoup

import lucene
from java.nio.file import Paths
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions


DATA_DIR = "raw_html_dataset"
INDEX_DIR = "lucene_index"


def get_html_text(file_path):
    with open(file_path, "rb") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
    body = soup.get_text(separator=" ", strip=True)

    return title, body


def create_index():
    if os.path.exists(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)

    os.mkdir(INDEX_DIR)

    store = SimpleFSDirectory(Paths.get(INDEX_DIR))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    meta_type = FieldType()
    meta_type.setStored(True)
    meta_type.setTokenized(False)

    text_type = FieldType()
    text_type.setStored(True)
    text_type.setTokenized(True)
    text_type.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    metadata_path = os.path.join(DATA_DIR, "metadata.jsonl")
    count = 0

    with open(metadata_path, "r", encoding="utf-8") as metadata_file:
        for line in metadata_file:
            record = json.loads(line)

            html_path = record.get("file_path", "").replace("\\", os.sep)

            if not os.path.exists(html_path):
                html_path = os.path.join(DATA_DIR, os.path.basename(html_path))

            if not os.path.exists(html_path):
                continue

            title, body = get_html_text(html_path)

            doc = Document()
            doc.add(Field("Title", str(title), text_type))
            doc.add(Field("Body", str(body), text_type))
            doc.add(Field("URL", str(record.get("url", "")), meta_type))
            doc.add(Field("Path", str(html_path), meta_type))

            writer.addDocument(doc)
            count += 1

    writer.close()
    print(f"Indexed {count} documents into {INDEX_DIR}")


if __name__ == "__main__":
    lucene.initVM(vmargs=["-Djava.awt.headless=true"])
    create_index()