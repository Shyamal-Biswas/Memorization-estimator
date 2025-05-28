
from flask import Flask, request, render_template
import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load embeddings and labels
embeddings = np.load("definition_embeddings.npy")
with open("definition_labels.json", "r") as f:
    labels = json.load(f)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Difficulty to time mapping
time_mapping = {
    "easy": (10, 13),
    "medium": (17, 20),
    "hard": (30, 35)
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form["definition"]
        user_vector = model.encode([user_input])
        _, indices = index.search(np.array(user_vector), k=5)
        top_labels = [labels[i] for i in indices[0]]
        difficulty = max(set(top_labels), key=top_labels.count)
        time_range = time_mapping[difficulty]
        exact_time = round(np.mean(time_range), 2)
        result = {
            "definition": user_input,
            "difficulty": difficulty,
            "time_range": f"{time_range[0]}–{time_range[1]} minutes",
            "exact_time": f"{exact_time} minutes"
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
