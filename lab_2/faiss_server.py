from flask import Flask, request, jsonify
import faiss
import numpy as np
import pickle
import os

app = Flask(__name__)

# Initialize FAISS index
dimension = 384
index = faiss.IndexFlatL2(dimension)
texts = []  # Store the actual text

INDEX_PATH = "/app/faiss_index/faiss.index"
TEXTS_PATH = "/app/faiss_index/texts.pkl"


def ensure_directory_exists():
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)


def load_index():
    global index, texts
    if os.path.exists(INDEX_PATH) and os.path.exists(TEXTS_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(TEXTS_PATH, "rb") as f:
            texts = pickle.load(f)
        print("Index and texts loaded successfully")
    else:
        print("No existing index found. Starting with empty index.")


@app.route("/add", methods=["POST"])
def add_vector():
    vector = np.array(request.json["vector"], dtype="float32")
    text = request.json["text"]
    index.add(vector.reshape(1, -1))
    texts.append(text)
    return jsonify({"status": "success", "index": len(texts) - 1})


@app.route("/search", methods=["POST"])
def search_vector():
    if index.ntotal == 0:
        return jsonify({"results": []})

    vector = np.array(request.json["vector"], dtype="float32")
    k = min(request.json.get("k", 5), index.ntotal)
    D, I = index.search(vector.reshape(1, -1), k)
    results = [
        {"index": int(i), "distance": float(d), "text": texts[int(i)]}
        for i, d in zip(I[0], D[0])
        if i != -1
    ]
    return jsonify({"results": results})


@app.route("/save", methods=["POST"])
def save_index():
    ensure_directory_exists()
    faiss.write_index(index, INDEX_PATH)
    with open(TEXTS_PATH, "wb") as f:
        pickle.dump(texts, f)
    return jsonify({"status": "success"})


@app.route("/load", methods=["POST"])
def load_index_route():
    load_index()
    return jsonify(
        {"status": "success", "message": "Index loaded (or initialized if not found)"}
    )


if __name__ == "__main__":
    load_index()
    app.run(host="0.0.0.0", port=5000)
