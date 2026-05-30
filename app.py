from flask import Flask, redirect, render_template, request, jsonify
import random, json, os, re
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "links.json")

def load_links():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_links(links):
    with open(DATA_FILE, "w") as f:
        json.dump(links, f)

def extract_video_id(url):
    url = url.strip()
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower().replace("www.", "")

        # youtu.be/VIDEO_ID
        if host == "youtu.be":
            vid = parsed.path.lstrip("/").split("/")[0]
            if re.match(r'^[a-zA-Z0-9_-]{11}$', vid):
                return vid

        if "youtube.com" in host:
            # /shorts/VIDEO_ID  or  /embed/VIDEO_ID  or  /v/VIDEO_ID
            m = re.match(r'^/(shorts|embed|v)/([a-zA-Z0-9_-]{11})', parsed.path)
            if m:
                return m.group(2)

            # /watch?v=VIDEO_ID&list=...&index=...  (any order of params)
            qs = parse_qs(parsed.query)
            if "v" in qs:
                vid = qs["v"][0]
                if re.match(r'^[a-zA-Z0-9_-]{11}$', vid):
                    return vid

    except Exception:
        pass
    return None

@app.route("/")
def index():
    links = load_links()
    return render_template("index.html", links=links)

@app.route("/go")
def go():
    links = load_links()
    if not links:
        return "<h2 style='font-family:sans-serif;text-align:center;margin-top:80px'>No videos added yet.<br><a href='/'>Go to dashboard</a></h2>"
    chosen = random.choice(links)
    # Direct YouTube redirect
    return redirect("https://www.youtube.com/watch?v=" + chosen["id"], code=302)

@app.route("/add", methods=["POST"])
def add():
    data = request.get_json(force=True)
    raw = data.get("urls", "")
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    links = load_links()
    existing_ids = {l["id"] for l in links}
    added = 0
    for url in lines:
        vid_id = extract_video_id(url)
        if vid_id and vid_id not in existing_ids:
            links.append({
                "id": vid_id,
                "url": "https://www.youtube.com/watch?v=" + vid_id,
                "thumbnail": f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg"
            })
            existing_ids.add(vid_id)
            added += 1
    save_links(links)
    return jsonify({"ok": True, "added": added, "total": len(links), "links": links})

@app.route("/delete/<vid_id>", methods=["POST"])
def delete(vid_id):
    links = [l for l in load_links() if l["id"] != vid_id]
    save_links(links)
    return jsonify({"ok": True, "total": len(links)})

@app.route("/clear", methods=["POST"])
def clear():
    save_links([])
    return jsonify({"ok": True, "total": 0})

@app.route("/links")
def get_links():
    return jsonify(load_links())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
