import lucene
from flask import Flask, render_template, request
from search import search_index

app = Flask(__name__)

lucene.initVM(vmargs=["-Djava.awt.headless=true"])


@app.route("/", methods=["GET", "POST"])
def home():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            lucene.getVMEnv().attachCurrentThread()
            results = search_index(query)

    return render_template("index.html", query=query, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)