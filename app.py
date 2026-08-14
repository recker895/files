











   





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












