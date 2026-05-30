from flask import Flask, redirect, render_template, request, jsonify, url_for
import random
import json
import os
import re

app = Flask(__name__)
DATA_FILE = "links.json"

def load_links():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_links(links):
    with open(DATA_FILE, "w") as f:
        json.dump(links, f)

def extract_video_id(url):
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def get_thumbnail(video_id):
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

@app.route("/")
def index():
    links = load_links()
    return render_template("index.html", links=links, count=len(links))

@app.route("/go")
def go():
    links = load_links()
    if not links:
        return render_template("empty.html")
    chosen = random.choice(links)
    return redirect(chosen["url"])

@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    raw = data.get("urls", "")
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    links = load_links()
    added = 0
    for url in lines:
        if "youtube.com" in url or "youtu.be" in url:
            vid_id = extract_video_id(url)
            if vid_id and not any(l["id"] == vid_id for l in links):
                links.append({
                    "id": vid_id,
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                    "thumbnail": get_thumbnail(vid_id)
                })
                added += 1
    save_links(links)
    return jsonify({"added": added, "total": len(links)})

@app.route("/delete/<vid_id>", methods=["POST"])
def delete(vid_id):
    links = load_links()
    links = [l for l in links if l["id"] != vid_id]
    save_links(links)
    return jsonify({"total": len(links)})

@app.route("/clear", methods=["POST"])
def clear():
    save_links([])
    return jsonify({"total": 0})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
