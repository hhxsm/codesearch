import os
import threading
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
import chardet
from elasticsearch import Elasticsearch

app = Flask(__name__)
CORS(app)

es = Elasticsearch("http://127.0.0.1:9200")
INDEX_NAME = "file_index"
indexing_status = {
    "running": False,
    "current": "",
    "count": 0
}

stop_flag = False
file_count = 0

EXCLUDE_DIRS = {"node_modules", ".git", "dist", "build", "__pycache__", ".idea", ".vscode"}
MAX_FILE_SIZE = 1000 * 1024 * 1024

def create_index():
    try:
        if es.indices.exists(index=INDEX_NAME):
            es.indices.delete(index=INDEX_NAME)
        es.indices.create(index=INDEX_NAME)
    except:
        pass

@app.route("/select_folder")
def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory()
    root.destroy()
    return jsonify({"folder": folder})

@app.route("/index_folders", methods=["POST"])
def index_folders():
    data = request.get_json()
    folders = data.get("folders", [])
    types = data.get("types", [])
    if not folders or not types:
        return jsonify({"ok": False})
    
    threading.Thread(target=index_multiple_folders, args=(folders, types), daemon=True).start()
    return jsonify({"ok": True})

def index_multiple_folders(folders, allowed_types):
    global indexing_status, stop_flag, file_count
    indexing_status["running"] = True
    indexing_status["count"] = 0
    file_count = 0
    stop_flag = False
    create_index()
    batch = []

    for folder in folders:
        if stop_flag:
            break
        for root_dir, dirs, files in os.walk(folder):
            if stop_flag:
                break
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if stop_flag:
                    break
                p = Path(root_dir) / file
                suffix = p.suffix.lower()
                if suffix not in allowed_types:
                    continue
                try:
                    if p.stat().st_size > MAX_FILE_SIZE:
                        continue
                except:
                    continue

                try:
                    file_count += 1
                    indexing_status["current"] = str(p)
                    with open(p, "rb") as f:
                        enc = chardet.detect(f.read(2048))["encoding"] or "utf-8"
                    with open(p, "r", encoding=enc, errors="ignore") as f:
                        lines = f.readlines()
                    for idx, line in enumerate(lines):
                        if stop_flag:
                            break
                        c = line.strip()
                        if not c:
                            continue
                        batch.append({"index": {"_index": INDEX_NAME}})
                        batch.append({"file": str(p), "line": idx + 1, "content": c})
                        if len(batch) >= 500:
                            es.bulk(body=batch)
                            batch = []
                            indexing_status["count"] += 500
                    if batch:
                        es.bulk(body=batch)
                        indexing_status["count"] += len(batch)
                        batch = []
                except Exception:
                    continue

    indexing_status["running"] = False
    if stop_flag:
        indexing_status["current"] = "建立索引已终止"
    else:
        indexing_status["current"] = f"建立索引完成 | 文件数：{file_count} | 总行数：{indexing_status['count']}"

@app.route("/stop_index", methods=["POST"])
def stop_index():
    global stop_flag
    stop_flag = True
    return jsonify({"ok": True})

@app.route("/index_status")
def index_status_route():
    return jsonify(indexing_status)

@app.route("/search", methods=["POST"])
def search():
    kw = request.json.get("keyword", "")
    res = es.search(
        index=INDEX_NAME,
        query={"match": {"content": kw}},
        size=10000
    )
    result = {}
    for hit in res["hits"]["hits"]:
        src = hit["_source"]
        f = src["file"]
        if f not in result:
            result[f] = []
        result[f].append({
            "line": src["line"],
            "content": src["content"]
        })
    return jsonify(result)

@app.route("/open_file", methods=["POST"])
def open_file():
    fp = request.json.get("file", "")
    try:
        import subprocess
        subprocess.run(['rundll32', 'shell32.dll,OpenAs_RunDLL', fp])
    except:
        pass
    return jsonify({"ok": True})

@app.route("/open_dir", methods=["POST"])
def open_dir():
    fp = request.json.get("file", "")
    try:
        os.startfile(os.path.dirname(fp))
    except:
        pass
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)