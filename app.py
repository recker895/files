











   
















@app.route("/search", 
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












