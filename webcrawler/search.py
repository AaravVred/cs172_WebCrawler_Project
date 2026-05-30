import lucene
from java.nio.file import Paths
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.queryparser.classic import QueryParser


INDEX_DIR = "lucene_index"


def search_index(query_text, max_results=10):
    search_dir = NIOFSDirectory(Paths.get(INDEX_DIR))
    searcher = IndexSearcher(DirectoryReader.open(search_dir))

    parser = QueryParser("Body", StandardAnalyzer())
    query = parser.parse(query_text)

    hits = searcher.search(query, max_results).scoreDocs
    results = []

    for hit in hits:
        doc = searcher.doc(hit.doc)

        results.append({
            "score": hit.score,
            "title": doc.get("Title"),
            "url": doc.get("URL"),
            "path": doc.get("Path")
        })

    return results


if __name__ == "__main__":
    lucene.initVM(vmargs=["-Djava.awt.headless=true"])

    query = input("Enter search query: ")
    results = search_index(query)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print(f"Score: {result['score']}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Path: {result['path']}")