










# --- Cosine similarity ---



# --- HTML UI ---

HTML = """



<h2>Semantic Search Engine (Python)</h2>

<textarea id="text" rows="6" placeholder="Paste text here"></textarea>

<button onclick="process()">Process</button>

<input id="query" placeholder="Search query">
<button onclick="search()">Search</button>

<div id="results"></div>

<script>
async function process() {
    const text = document.getElementById("text").value;

    await fetch("/process", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    alert("Text processed");
}

async function search() {
    const query = document.getElementById("query").value;

    const res = await fetch("/search", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query})
    });

    const data = await res.json();

    const div = document.getElementById("results");
    div.innerHTML = "";

    data.forEach(r => {
        div.innerHTML += `
            <div class="result">
                <div>Score: ${r.score.toFixed(3)}</div>
                <div>${r.text}</div>
            </div>
        `;
    });
}
</script>

</body>
</html>
"""

# --- Routes ---

@app.route("/")
def home():
return render_template_string(HTML)

@app.route("/process", methods=["POST"])
def process_text():
global chunks, vectors
text = request.json["text"]

```
chunks = re.findall(r'.{1,200}', text)
vectors = [embed(c) for c in chunks]

return jsonify({"status": "ok"})
```

@app.route("/search", methods=["POST"])
def search():
query = request.json["query"]
q_vec = embed(query)

```
scores = []
for i, vec in enumerate(vectors):
    score = cosine_sim(q_vec, vec)
    scores.append({"text": chunks[i], "score": score})

scores.sort(key=lambda x: x["score"], reverse=True)

return jsonify(scores[:5])
```

if **name** == "**main**":
app.run(debug=True) 












